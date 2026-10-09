from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SubjectChoices(models.TextChoices):
    PROGRAMMING = 'PROGRAMMING', 'PROGRAMMING'
    LANGUAGE = 'LANGUAGE', 'LANGUAGE'
    ACADEMIC = 'ACADEMIC', 'ACADEMIC'
    INTERVIEW = 'INTERVIEW', 'INTERVIEW'
    OTHER = 'OTHER', 'OTHER'

class Deck(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="decks")
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    subject = models.CharField(
        max_length=20,
        choices=SubjectChoices.choices,
        default=SubjectChoices.OTHER
    )
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name="cards")
    front = models.TextField()
    back = models.TextField()
    hint = models.CharField(max_length=200, blank=True)
    box = models.PositiveSmallIntegerField(default=1)
    next_review_at = models.DateTimeField(default=timezone.now)
    last_reviewed_at = models.DateTimeField(null=True, blank=True)
    times_reviewed = models.PositiveIntegerField(default=0)
    times_correct = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["box", "next_review_at"]

    def __str__(self):
        return self.front[:40]


class ReviewLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_logs")
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, blank=True, related_name="review_logs")
    box_before = models.PositiveSmallIntegerField()
    box_after = models.PositiveSmallIntegerField()
    is_correct = models.BooleanField()
    reviewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-reviewed_at"]

    def __str__(self):
        return f"{self.user.username} reviewed {self.card_id} at {self.reviewed_at}"
