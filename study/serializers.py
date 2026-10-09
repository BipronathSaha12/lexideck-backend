from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Deck, Card

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class DeckSerializer(serializers.ModelSerializer):
    card_count = serializers.IntegerField(read_only=True)
    due_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Deck
        fields = [
            "id", "title", "description", "subject", "is_archived", 
            "card_count", "due_count", "created_at", "updated_at"
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate_title(self, value):
        qs = Deck.objects.filter(owner=self.context["request"].user, title__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("You already have a deck with this title.")
        return value


class CardSerializer(serializers.ModelSerializer):
    deck_title = serializers.CharField(source="deck.title", read_only=True)
    is_due = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = [
            "id", "deck", "deck_title", "front", "back", "hint",
            "box", "next_review_at", "last_reviewed_at", 
            "times_reviewed", "times_correct", "is_due", 
            "created_at", "updated_at"
        ]
        read_only_fields = [
            "box", "next_review_at", "last_reviewed_at", 
            "times_reviewed", "times_correct", "created_at", "updated_at"
        ]

    def get_is_due(self, obj):
        return obj.next_review_at <= timezone.now()

    def validate_deck(self, deck):
        if deck.owner != self.context["request"].user:
            raise serializers.ValidationError("This deck does not belong to you.")
        return deck
