from django.contrib import admin
from .models import Deck, Card

admin.site.register(Deck)

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("front", "deck", "box", "next_review_at")
