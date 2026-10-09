from rest_framework import viewsets, status, filters, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Count, Q, Sum
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth.models import User
from .models import Deck, Card
from .serializers import RegisterSerializer, DeckSerializer, CardSerializer

INTERVALS = {1: 0, 2: 1, 3: 3, 4: 7, 5: 16}

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class DeckViewSet(viewsets.ModelViewSet):
    serializer_class = DeckSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["subject", "is_archived"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        now = timezone.now()
        return (Deck.objects
            .filter(owner=self.request.user)
            .annotate(
                card_count=Count("cards", distinct=True),
                due_count=Count("cards", filter=Q(cards__next_review_at__lte=now), distinct=True),
            ))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["get"])
    def study(self, request, pk=None):
        deck = self.get_object()
        now = timezone.now()
        cards_qs = deck.cards.filter(next_review_at__lte=now).order_by("next_review_at")[:20]
        serializer = CardSerializer(cards_qs, many=True, context={'request': request})
        
        return Response({
            "deck": {"id": deck.id, "title": deck.title},
            "due_count": deck.cards.filter(next_review_at__lte=now).count(),
            "cards": serializer.data
        })


class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["deck", "box"]
    search_fields = ["front", "back"]
    ordering_fields = ["created_at", "box", "next_review_at"]
    ordering = ["box", "next_review_at"]

    def get_queryset(self):
        return Card.objects.filter(deck__owner=self.request.user).select_related("deck")

    @action(detail=True, methods=["post"])
    def review(self, request, pk=None):
        card = self.get_object()
        correct = request.data.get("correct")
        
        if not isinstance(correct, bool):
            return Response(
                {"correct": ["This field is required and must be true or false."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        box_before = card.box
        card.box = min(card.box + 1, 5) if correct else 1
        card.next_review_at = timezone.now() + timedelta(days=INTERVALS[card.box])
        card.last_reviewed_at = timezone.now()
        card.times_reviewed += 1
        if correct:
            card.times_correct += 1
        card.save()

        from .models import ReviewLog
        ReviewLog.objects.create(
            user=request.user,
            card=card,
            box_before=box_before,
            box_after=card.box,
            is_correct=correct
        )
        
        return Response(self.get_serializer(card).data)


class StatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cards = Card.objects.filter(deck__owner=request.user)
        rows = cards.values("box").annotate(n=Count("id"))
        boxes = {str(i): 0 for i in range(1, 6)}
        for row in rows:
            boxes[str(row["box"])] = row["n"]
            
        totals = cards.aggregate(r=Sum("times_reviewed"), c=Sum("times_correct"))
        reviewed, correct = totals["r"] or 0, totals["c"] or 0
        
        from .models import ReviewLog
        from django.db.models.functions import TruncDate
        thirty_days_ago = timezone.now() - timedelta(days=30)
        logs = ReviewLog.objects.filter(user=request.user, reviewed_at__gte=thirty_days_ago)
        daily_counts = logs.annotate(date=TruncDate('reviewed_at')).values('date').annotate(count=Count('id')).order_by('date')
        heatmap = {str(item['date']): item['count'] for item in daily_counts}
        
        return Response({
            "user": {
                "username": request.user.username,
                "email": request.user.email,
            },
            "decks": Deck.objects.filter(owner=request.user).count(),
            "cards": cards.count(),
            "due_now": cards.filter(next_review_at__lte=timezone.now()).count(),
            "mastered": boxes["5"],
            "reviewed_today": cards.filter(last_reviewed_at__date=timezone.localdate()).count(),
            "accuracy": round(100 * correct / reviewed) if reviewed else 0,
            "boxes": boxes,
            "heatmap": heatmap,
        })
