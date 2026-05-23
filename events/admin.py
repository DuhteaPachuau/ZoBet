from django.contrib import admin
from .models import Event, Team

class TeamInline(admin.TabularInline):
    model = Team
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'entry_fee', 'prize_pool', 'participant_count', 'created_at']
    list_filter = ['status']
    search_fields = ['title']
    inlines = [TeamInline]
    fieldsets = [
        ('Basic Info', {'fields': ['title', 'description', 'banner']}),
        ('Pricing', {'fields': ['entry_fee', 'commission_percentage', 'prize_pool']}),
        ('Schedule', {'fields': ['prediction_deadline', 'start_date', 'end_date']}),
        ('Settings', {'fields': ['status', 'featured', 'max_participants']}),
    ]

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'short_code']
    search_fields = ['name', 'event__title']
