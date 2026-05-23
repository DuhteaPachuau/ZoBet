from django.contrib import admin
from .models import Wallet, Transaction, WithdrawalRequest

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'locked_balance', 'is_locked']
    list_filter = ['is_locked']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'transaction_type', 'status', 'created_at']
    list_filter = ['transaction_type', 'status']
    search_fields = ['user__username', 'payment_id']

@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'upi_id', 'status', 'created_at']
    list_filter = ['status']
    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        for wr in queryset.filter(status='pending'):
            wallet = wr.user.wallet
            wallet.balance -= wr.amount
            wallet.save()
            from wallet.models import Transaction
            Transaction.objects.create(
                user=wr.user,
                amount=wr.amount,
                transaction_type='withdrawal',
                description=f'Withdrawal request approved',
                balance_after=wallet.balance
            )
        queryset.update(status='approved')
    approve_requests.short_description = "Approve selected withdrawal requests"

    def reject_requests(self, request, queryset):
        queryset.update(status='rejected')
    reject_requests.short_description = "Reject selected withdrawal requests"
