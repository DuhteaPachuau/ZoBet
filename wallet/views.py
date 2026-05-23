from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wallet, Transaction, WithdrawalRequest
from notifications.models import Notification

@login_required
def wallet_view(request):
    wallet = request.user.wallet
    transactions = Transaction.objects.filter(user=request.user)[:20]
    return render(request, 'wallet/wallet.html', {
        'wallet': wallet,
        'transactions': transactions
    })

@login_required
def deposit_view(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount = float(amount)
            if amount < 1:
                messages.error(request, 'Minimum deposit is ₹1.')
                return redirect('wallet:deposit')
            wallet = request.user.wallet
            wallet.add_funds(amount, 'Deposit', transaction_type='deposit')
            messages.success(request, f'₹{amount:.2f} deposited successfully!')
            return redirect('wallet:wallet')
        except (ValueError, TypeError):
            messages.error(request, 'Invalid amount.')
    return render(request, 'wallet/deposit.html')

@login_required
def withdraw_view(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        upi_id = request.POST.get('upi_id')
        account_holder = request.POST.get('account_holder')

        try:
            amount = float(amount)
            if amount < 100:
                messages.error(request, 'Minimum withdrawal amount is ₹100.')
                return redirect('wallet:withdraw')
            if amount > request.user.wallet.available_balance:
                messages.error(request, 'Insufficient balance.')
                return redirect('wallet:withdraw')

            wallet = request.user.wallet
            wallet.locked_balance += amount
            wallet.save()

            WithdrawalRequest.objects.create(
                user=request.user,
                amount=amount,
                upi_id=upi_id,
                account_holder=account_holder
            )
            messages.success(request, f'Withdrawal request for ₹{amount} submitted successfully!')
            return redirect('wallet:wallet')
        except ValueError:
            messages.error(request, 'Invalid amount.')

    return render(request, 'wallet/withdraw.html')

@login_required
def transaction_history_view(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'wallet/transactions.html', {'transactions': transactions})
