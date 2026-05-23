from django.conf import settings
from wallet.models import WithdrawalRequest

def site_settings(request):
    ctx = {
        'site_name': settings.SITE_NAME,
        'site_url': settings.SITE_URL,
    }
    if request.user.is_staff:
        ctx['pending_withdrawals_count'] = WithdrawalRequest.objects.filter(status='pending').count()
    return ctx
