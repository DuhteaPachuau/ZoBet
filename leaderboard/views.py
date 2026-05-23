from django.shortcuts import render
from accounts.models import Profile
from django.db.models import F, ExpressionWrapper, FloatField, Value, Q, Case, When
from datetime import timedelta
from django.utils import timezone

def leaderboard_view(request):
    period = request.GET.get('period', 'all')

    profiles = Profile.objects.select_related('user').filter(total_predictions__gt=0)

    if period == 'monthly':
        month_ago = timezone.now() - timedelta(days=30)
        profiles = profiles.filter(
            user__predictions__created_at__gte=month_ago
        ).distinct()

    top_earners = profiles.order_by('-total_winnings')[:20]

    top_accuracy = profiles.annotate(
        win_rate_calc=ExpressionWrapper(
            F('correct_predictions') * 100.0 / F('total_predictions'),
            output_field=FloatField()
        )
    ).order_by('-win_rate_calc')[:20]

    for i, p in enumerate(top_earners, 1):
        p.rank = i
    for i, p in enumerate(top_accuracy, 1):
        p.acc_rank = i

    return render(request, 'leaderboard/leaderboard.html', {
        'top_earners': top_earners,
        'top_accuracy': top_accuracy,
        'current_period': period,
    })
