from django.contrib import admin
from .models import Prediction

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'team', 'is_correct', 'reward_amount', 'created_at']
    list_filter = ['is_correct']
    search_fields = ['user__username', 'event__title', 'team__name']
