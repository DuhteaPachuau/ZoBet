import json, hashlib, hmac
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from wallet.models import Wallet, Transaction
from notifications.models import Notification
import razorpay

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def create_order_view(request):
    if request.method == 'POST':
        amount = int(float(request.POST.get('amount')) * 100)
        if amount < 100:
            return JsonResponse({'error': 'Minimum deposit is ₹1'}, status=400)

        order = razorpay_client.order.create({
            'amount': amount,
            'currency': 'INR',
            'payment_capture': '1',
            'notes': {
                'user_id': str(request.user.id),
                'username': request.user.username,
            }
        })

        return JsonResponse({
            'order_id': order['id'],
            'amount': amount,
            'currency': 'INR',
            'key_id': settings.RAZORPAY_KEY_ID,
        })

@csrf_exempt
def payment_webhook_view(request):
    if request.method == 'POST':
        body = request.body
        sig = request.headers.get('X-Razorpay-Signature')
        secret = settings.RAZORPAY_KEY_SECRET

        expected_sig = hmac.new(
            secret.encode(),
            body,
            hashlib.sha256
        ).hexdigest()

        if sig == expected_sig:
            data = json.loads(body)
            event_type = data.get('event')

            if event_type == 'payment.captured':
                payload = data.get('payload', {}).get('payment', {}).get('entity', {})
                order_id = payload.get('order_id')
                payment_id = payload.get('id')
                amount = float(payload.get('amount', 0)) / 100

                try:
                    order = razorpay_client.order.fetch(order_id)
                    notes = order.get('notes', {})
                    user_id = notes.get('user_id')

                    if user_id:
                        from django.contrib.auth.models import User
                        user = User.objects.get(id=user_id)
                        wallet = user.wallet
                        wallet.add_funds(amount, f'Deposit via Razorpay ({payment_id})', transaction_type='deposit')

                        Notification.objects.create(
                            user=user,
                            notification_type='payment',
                            title='Deposit Successful!',
                            message=f'₹{amount:.2f} has been added to your wallet.'
                        )
                except Exception:
                    pass

            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'invalid signature'}, status=400)

    return JsonResponse({'status': 'invalid method'}, status=405)

@login_required
def payment_success_view(request):
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')
    amount = float(request.GET.get('amount', 0))

    if payment_id and amount > 0:
        wallet = request.user.wallet

        if Transaction.objects.filter(payment_id=payment_id).exists():
            messages.info(request, 'This payment has already been processed.')
            return redirect('wallet:wallet')

        wallet.add_funds(amount, f'Deposit via Razorpay ({payment_id})', transaction_type='deposit')
        Transaction.objects.filter(user=request.user, amount=amount, description=f'Deposit via Razorpay ({payment_id})').update(payment_id=payment_id)

        Notification.objects.create(
            user=request.user,
            notification_type='payment',
            title='Deposit Successful!',
            message=f'₹{amount:.2f} has been added to your wallet.'
        )

        messages.success(request, f'₹{amount:.2f} deposited successfully!')
    else:
        messages.error(request, 'Invalid payment response.')
    return redirect('wallet:wallet')
