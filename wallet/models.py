from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    locked_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s wallet - ₹{self.balance}"

    @property
    def available_balance(self):
        return self.balance - self.locked_balance

    def can_deduct(self, amount):
        return self.available_balance >= amount

    def deduct(self, amount, description="", transaction_type='event_entry'):
        if not self.can_deduct(amount):
            raise ValueError("Insufficient balance")
        self.balance -= Decimal(str(amount))
        self.save()
        Transaction.objects.create(
            user=self.user,
            amount=amount,
            transaction_type=transaction_type,
            description=description,
            balance_after=self.balance
        )

    def add_funds(self, amount, description="", transaction_type='reward'):
        self.balance += Decimal(str(amount))
        self.save()
        Transaction.objects.create(
            user=self.user,
            amount=amount,
            transaction_type=transaction_type,
            description=description,
            balance_after=self.balance
        )

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('event_entry', 'Event Entry Fee'),
        ('reward', 'Prize Reward'),
        ('refund', 'Refund'),
        ('referral_bonus', 'Referral Bonus'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=255)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, default='completed')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - ₹{self.amount}"

class WithdrawalRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawal_requests')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    upi_id = models.CharField(max_length=100)
    account_holder = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - ₹{self.amount} - {self.status}"
