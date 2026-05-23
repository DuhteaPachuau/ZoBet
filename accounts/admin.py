from django.contrib import admin
from .models import Profile, Referral

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'referral_code', 'total_winnings', 'win_rate', 'created_at']
    search_fields = ['user__username', 'referral_code']

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['referrer', 'referred', 'bonus_earned', 'created_at']
