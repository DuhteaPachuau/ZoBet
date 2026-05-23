from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Event(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('live', 'Live'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    banner = models.ImageField(upload_to='zobet/events/banners/', blank=True, null=True)
    entry_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Minimum Bet (₹)')
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    prize_pool = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    show_prize_pool = models.BooleanField(default=True)

    prediction_deadline = models.DateTimeField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    winner = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='won_events')
    winner_declared = models.BooleanField(default=False)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    featured = models.BooleanField(default=False)
    max_participants = models.IntegerField(default=0, help_text='0 = unlimited')
    participant_count = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_prediction_open(self):
        return timezone.now() < self.prediction_deadline and self.status in ['upcoming', 'live']

    @property
    def total_prize_pool(self):
        return self.prize_pool

    @property
    def time_remaining(self):
        delta = self.start_date - timezone.now()
        return delta

    def save(self, *args, **kwargs):
        if self.status == 'upcoming' and timezone.now() >= self.start_date:
            self.status = 'live'
        if self.status == 'live' and timezone.now() >= self.end_date:
            self.status = 'completed'
        super().save(*args, **kwargs)

class Team(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='zobet/events/teams/', blank=True, null=True)
    description = models.TextField(blank=True)
    short_code = models.CharField(max_length=10, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.event.title})"
