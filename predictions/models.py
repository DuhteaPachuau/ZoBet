from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='predictions')
    team = models.ForeignKey('events.Team', on_delete=models.CASCADE, related_name='predictions')
    bet_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_correct = models.BooleanField(null=True, blank=True)
    reward_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} -> {self.team.name} ({self.event.title})"

    def clean(self):
        if self.event and not self.event.is_prediction_open:
            raise ValidationError("Prediction deadline has passed")
        if self.event and self.event.status == 'completed':
            raise ValidationError("This event has already completed")

    def save(self, *args, **kwargs):
        if not self.pk:
            self.event.participant_count = self.event.predictions.count() + 1
            self.event.save()
        super().save(*args, **kwargs)
