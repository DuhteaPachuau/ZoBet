from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from django.db import models, IntegrityError
from .models import Event, Team
from .forms import EventForm, TeamForm
from predictions.models import Prediction
from wallet.models import Wallet, Transaction
from notifications.models import Notification
from decimal import Decimal

def event_list_view(request):
    events = Event.objects.all()
    upcoming = events.filter(status='upcoming')
    live = events.filter(status='live')
    completed = events.filter(status='completed')

    context = {
        'upcoming_events': upcoming,
        'live_events': live,
        'completed_events': completed,
    }
    return render(request, 'events/event_list.html', context)

def event_detail_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    teams = event.teams.all()
    user_prediction = None
    can_predict = False

    if request.user.is_authenticated:
        try:
            user_prediction = Prediction.objects.get(user=request.user, event=event)
        except Prediction.DoesNotExist:
            pass
        can_predict = event.is_prediction_open and user_prediction is None

    context = {
        'event': event,
        'teams': teams,
        'user_prediction': user_prediction,
        'can_predict': can_predict,
    }
    return render(request, 'events/event_detail.html', context)

@login_required
def predict_view(request, event_id, team_id):
    event = get_object_or_404(Event, id=event_id)
    team = get_object_or_404(Team, id=team_id, event=event)

    if not event.is_prediction_open:
        messages.error(request, 'Prediction deadline has passed for this event.')
        return redirect('events:detail', event_id=event.id)

    bet_amount = Decimal(request.POST.get('bet_amount', '0'))
    min_bet = Decimal(str(event.entry_fee))

    if bet_amount < min_bet:
        messages.error(request, f'Minimum bet amount is ₹{event.entry_fee}.')
        return redirect('events:detail', event_id=event.id)

    wallet = request.user.wallet
    if not wallet.can_deduct(bet_amount):
        messages.error(request, 'Insufficient wallet balance. Please deposit money first.')
        return redirect('wallet:deposit')

    try:
        prediction = Prediction.objects.create(user=request.user, event=event, team=team, bet_amount=bet_amount)
        wallet.deduct(bet_amount, f'Bet for {event.title} - {team.name}')
        event.prize_pool += bet_amount
        event.participant_count += 1
        event.save()
        profile = request.user.profile
        profile.total_predictions += 1
        profile.save()
        messages.success(request, f'Your prediction for {team.name} with ₹{bet_amount} bet is submitted!')
        Notification.objects.create(
            user=request.user,
            notification_type='prediction',
            title='Prediction Submitted!',
            message=f'You bet ₹{bet_amount} on {team.name} for {event.title}. Good luck!'
        )
    except IntegrityError:
        messages.error(request, 'You have already made a prediction for this event.')
    return redirect('events:detail', event_id=event.id)

@staff_member_required
def declare_winner_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        team_id = request.POST.get('winner_team')
        if not team_id:
            messages.error(request, 'Please select a winning team.')
            return redirect('events:detail', event_id=event.id)

        winner_team = get_object_or_404(Team, id=team_id, event=event)
        event.winner = winner_team
        event.winner_declared = True
        event.status = 'completed'

        total_predictions_count = Prediction.objects.filter(event=event).count()
        correct_predictions = Prediction.objects.filter(event=event, team=winner_team)
        total_correct = correct_predictions.count()
        total_pool = event.prize_pool
        if total_predictions_count <= 1:
            commission = Decimal('0')
        else:
            commission = total_pool * (event.commission_percentage / 100)
        reward_pool = total_pool - commission

        if total_correct > 0:
            total_bet_of_winners = correct_predictions.aggregate(total=models.Sum('bet_amount'))['total'] or Decimal('0')
            for pred in correct_predictions:
                share = (pred.bet_amount / total_bet_of_winners) * reward_pool if total_bet_of_winners > 0 else Decimal('0')
                pred.is_correct = True
                pred.reward_amount = share
                pred.save()

                wallet = pred.user.wallet
                wallet.add_funds(share, f'Won prediction for {event.title}')
                profile = pred.user.profile
                profile.total_winnings += share
                profile.correct_predictions += 1
                profile.win_streak += 1
                profile.save()

                Notification.objects.create(
                    user=pred.user,
                    notification_type='reward',
                    title='You Won! 🎉',
                    message=f'Congratulations! You won ₹{share:.2f} for correctly predicting {winner_team.name} in {event.title}!'
                )

        incorrect_predictions = Prediction.objects.filter(event=event).exclude(team=winner_team)
        for pred in incorrect_predictions:
            pred.is_correct = False
            pred.save()
            profile = pred.user.profile
            profile.win_streak = 0
            profile.save()
            Notification.objects.create(
                user=pred.user,
                notification_type='prediction',
                title='Result Declared',
                message=f'{winner_team.name} won {event.title}. Your prediction was not correct this time.'
            )

        if commission > 0:
            admin_wallet = event.created_by.wallet
            admin_wallet.add_funds(commission, f'Commission from {event.title}')
            admin_profile = event.created_by.profile
            admin_profile.total_winnings += commission
            admin_profile.save()
            Notification.objects.create(
                user=event.created_by,
                notification_type='reward',
                title='Commission Earned!',
                message=f'You earned ₹{commission:.2f} commission from {event.title}'
            )

        event.save()
        messages.success(request, f'{winner_team.name} declared as champion! Rewards distributed.')
    return redirect('events:detail', event_id=event.id)

@staff_member_required
@staff_member_required
def create_event_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                event = form.save(commit=False)
                event.created_by = request.user
                event.save()
                messages.success(request, 'Event created successfully! Add teams now.')
                return redirect('events:add_teams', event_id=event.id)
            except Exception as e:
                messages.error(request, f'Error creating event: {e}')
                return redirect('events:create_event')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form, 'editing': False})

@staff_member_required
def edit_event_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('events:detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/create_event.html', {'form': form, 'editing': True, 'event': event})

@staff_member_required
def add_teams_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save(commit=False)
            team.event = event
            team.save()
            messages.success(request, f'Team "{team.name}" added!')
            return redirect('events:add_teams', event_id=event.id)
    else:
        form = TeamForm()
    teams = event.teams.all()
    return render(request, 'events/add_teams.html', {'form': form, 'event': event, 'teams': teams})
