from django.shortcuts import render

def terms_view(request):
    return render(request, 'pages/terms.html')

def privacy_view(request):
    return render(request, 'pages/privacy.html')

def contact_view(request):
    return render(request, 'pages/contact.html')

def how_it_works_view(request):
    return render(request, 'pages/how_it_works.html')

def faq_view(request):
    faqs = [
        {'q': 'What is ZoBet?', 'a': 'ZoBet is a tournament prediction platform where users predict winning teams of sports events and win real prize money from the prize pool.'},
        {'q': 'How do I start predicting?', 'a': 'Create an account, deposit funds into your wallet, browse active events, pick your champion before the deadline, and pay the entry fee.'},
        {'q': 'How is the prize distributed?', 'a': 'When the admin declares a winner, the platform commission is deducted from the total pool. The remaining amount is split proportionally based on each winner\'s bet amount — the more you bet, the more you win.'},
        {'q': 'What payment methods are accepted?', 'a': 'We support deposits via UPI, credit/debit cards, and net banking through our Razorpay payment gateway. Withdrawals are processed to your UPI account.'},
        {'q': 'How long do withdrawals take?', 'a': 'Withdrawal requests are typically processed within 24-48 hours after approval by our team.'},
        {'q': 'Is there a minimum withdrawal amount?', 'a': 'No, you can withdraw any amount from your wallet. There is no minimum withdrawal limit.'},
        {'q': 'Can I change my prediction?', 'a': 'No, predictions are final once submitted. Make sure to review your choice before confirming.'},
        {'q': 'What happens if no one predicts correctly?', 'a': 'If no user predicts the winning champion, the prize pool remains in the platform. The entry fees are not returned.'},
        {'q': 'How does the referral system work?', 'a': 'Share your unique referral code with friends. When they register and start predicting, you earn a ₹50 bonus credited to your wallet.'},
        {'q': 'Is my data safe?', 'a': 'Yes, we use industry-standard encryption and security practices. Your financial information is processed securely through Razorpay.'},
    ]
    return render(request, 'pages/faq.html', {'faq_items': faqs})

def about_view(request):
    return render(request, 'pages/about.html')
