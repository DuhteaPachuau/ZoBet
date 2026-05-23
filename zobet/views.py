from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from events.models import Event, Team
from wallet.models import Transaction, WithdrawalRequest, Wallet
from predictions.models import Prediction
from accounts.models import Profile
from notifications.models import Notification
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta

def home_view(request):
    events = Event.objects.all()
    upcoming = Event.objects.filter(status='upcoming')[:6]
    live = Event.objects.filter(status='live')[:6]
    total_prize_pool = sum(e.prize_pool for e in events)
    total_participants = sum(e.participant_count for e in events)
    top_users = Profile.objects.select_related('user').order_by('-total_winnings')[:5]

    return render(request, 'home.html', {
        'upcoming_events': upcoming,
        'live_events': live,
        'all_events': events[:8],
        'total_prize_pool': total_prize_pool,
        'total_participants': total_participants,
        'total_events': events.count(),
        'top_users': top_users,
    })

@staff_member_required
def admin_events_view(request):
    events = Event.objects.all().order_by('-created_at')
    return render(request, 'admin_dashboard/events.html', {'events': events})

@staff_member_required
def delete_event_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    messages.success(request, f'Event "{event.title}" deleted successfully.')
    return redirect('admin_events')

@staff_member_required
def admin_withdrawals_view(request):
    withdrawals = WithdrawalRequest.objects.all().order_by('-created_at')
    return render(request, 'admin_dashboard/withdrawals.html', {'withdrawals': withdrawals})

@staff_member_required
def admin_users_view(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_dashboard/users.html', {'users': users})

@staff_member_required
def approve_withdrawal_view(request, withdrawal_id):
    wr = get_object_or_404(WithdrawalRequest, id=withdrawal_id, status='pending')
    wallet = wr.user.wallet
    wallet.balance -= wr.amount
    wallet.locked_balance -= wr.amount
    wallet.save()
    wr.status = 'completed'
    wr.save()
    Transaction.objects.create(
        user=wr.user, amount=wr.amount, transaction_type='withdrawal',
        description=f'Withdrawal to {wr.upi_id} approved',
        balance_after=wallet.balance
    )
    Notification.objects.create(
        user=wr.user, notification_type='withdrawal',
        title='Withdrawal Approved!',
        message=f'Your withdrawal of ₹{wr.amount} has been processed.'
    )
    messages.success(request, f'Withdrawal ₹{wr.amount} approved for {wr.user.username}')
    return redirect('admin_withdrawals')

@staff_member_required
def reject_withdrawal_view(request, withdrawal_id):
    wr = get_object_or_404(WithdrawalRequest, id=withdrawal_id, status='pending')
    wallet = wr.user.wallet
    wallet.locked_balance -= wr.amount
    wallet.save()
    wr.status = 'rejected'
    wr.save()
    Notification.objects.create(
        user=wr.user, notification_type='withdrawal',
        title='Withdrawal Rejected',
        message=f'Your withdrawal of ₹{wr.amount} has been rejected.'
    )
    messages.warning(request, f'Withdrawal ₹{wr.amount} rejected for {wr.user.username}')
    return redirect('admin_withdrawals')

@staff_member_required
def admin_dashboard_view(request):
    total_users = User.objects.count()
    total_events = Event.objects.count()
    active_events = Event.objects.filter(status='live').count()
    completed_events = Event.objects.filter(status='completed').count()
    total_revenue = Wallet.objects.aggregate(Sum('balance'))['balance__sum'] or 0
    total_deposits = Transaction.objects.filter(transaction_type='deposit').aggregate(Sum('amount'))['amount__sum'] or 0
    total_withdrawals = Transaction.objects.filter(transaction_type='withdrawal').aggregate(Sum('amount'))['amount__sum'] or 0
    pending_withdrawals_count = WithdrawalRequest.objects.filter(status='pending').count()
    total_predictions = Prediction.objects.count()
    correct_predictions = Prediction.objects.filter(is_correct=True).count()

    today = timezone.now()
    month_ago = today - timedelta(days=30)
    new_users_this_month = User.objects.filter(date_joined__gte=month_ago).count()
    revenue_this_month = Transaction.objects.filter(
        transaction_type='deposit', created_at__gte=month_ago
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    recent_users = User.objects.order_by('-date_joined')[:5]
    pending_withdrawals = WithdrawalRequest.objects.filter(status='pending')[:5]
    recent_transactions = Transaction.objects.order_by('-created_at')[:5]
    recent_events_list = Event.objects.order_by('-created_at')[:5]

    context = {
        'total_users': total_users,
        'total_events': total_events,
        'active_events': active_events,
        'completed_events': completed_events,
        'total_revenue': total_revenue,
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
        'pending_withdrawals_count': pending_withdrawals_count,
        'total_predictions': total_predictions,
        'correct_predictions': correct_predictions,
        'new_users_this_month': new_users_this_month,
        'revenue_this_month': revenue_this_month,
        'recent_users': recent_users,
        'pending_withdrawals': pending_withdrawals,
        'recent_transactions': recent_transactions,
        'recent_events': recent_events_list,
    }
    return render(request, 'admin_dashboard/overview.html', context)
