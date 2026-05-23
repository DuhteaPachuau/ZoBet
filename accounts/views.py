from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from .models import Profile

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Welcome to ZoBet!')
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})

@login_required
def dashboard_view(request):
    user = request.user
    profile = user.profile
    wallet = user.wallet
    all_predictions = user.predictions.all()
    transactions = user.transactions.all()[:10]
    notifications = user.notifications.filter(is_read=False)[:5]

    total_predictions = all_predictions.count()
    correct = all_predictions.filter(is_correct=True).count()
    pending = all_predictions.filter(is_correct__isnull=True).count()
    predictions = all_predictions[:10]

    context = {
        'profile': profile,
        'wallet': wallet,
        'predictions': predictions,
        'transactions': transactions,
        'notifications': notifications,
        'total_predictions': total_predictions,
        'correct_predictions': correct,
        'pending_predictions': pending,
        'win_rate': profile.win_rate,
    }
    return render(request, 'dashboard/dashboard.html', context)
