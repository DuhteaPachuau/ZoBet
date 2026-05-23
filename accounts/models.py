from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid, random, string

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='zobet/profiles/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, blank=True)
    referral_code = models.CharField(max_length=20, unique=True, blank=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    total_winnings = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_predictions = models.IntegerField(default=0)
    correct_predictions = models.IntegerField(default=0)
    win_streak = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def win_rate(self):
        if self.total_predictions == 0:
            return 0
        return round((self.correct_predictions / self.total_predictions) * 100, 1)

    def generate_referral_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_referral_code()
        super().save(*args, **kwargs)

class Referral(models.Model):
    referrer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='referrer_profiles')
    referred = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='referred_profiles')
    bonus_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        from wallet.models import Wallet
        Wallet.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except:
        pass
