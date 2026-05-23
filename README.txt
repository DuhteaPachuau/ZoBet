============================================
ZoBet - Tournament Prediction Platform
============================================

=== DONE ===

[Core]
- Django project with 7 apps: accounts, events, wallet, predictions, payments, leaderboard, notifications
- User registration/login/logout with profile (image, phone, referral code)
- Auto-creation of Profile & Wallet via signals on user registration
- Home page with hero, live/upcoming events, top predictors

[Events & Predictions]
- Event CRUD (admin creates/edits events, adds teams)
- Prediction system: select team, entry fee deducted from wallet, deadline check
- Declare winner: auto-distributes rewards from prize pool, admin gets commission
- Prize pool tracking, participant count

[Wallet]
- Deposit (direct server-side, no Razorpay popup)
- Withdrawal request with admin approval/rejection
- Transaction history with +/- display (green for credits, red for debits)
- Wallet balance visible in navbar

[Leaderboard]
- Top earners and accuracy rankings using DB annotation

[Notifications]
- Per-user notifications (reward, payment, prediction, withdrawal, referral, system)
- Unread count polling every 30s, bell icon in navbar

[Admin Dashboard]
- /admin-dashboard/ with Overview, Events, Withdrawals, Users tabs
- Approve/reject withdrawals, view users, manage events
- Mobile tab bar + desktop sidebar

[Auth & Social]
- django-allauth for Google login (configured, working)
- Forgot password via Django PasswordResetView (emails to console)

[UI/UX]
- Tailwind CSS + glassmorphism dark sports theme
- Responsive mobile-first design with hamburger menu
- Static pages: Terms, Privacy, Contact (WhatsApp), How It Works, FAQ, About
- All inputs consistently styled

=== TODO (Before Production) ===

1. DEPLOY TO SERVER
   - Buy domain + hosting
   - Set up PostgreSQL (optional, SQLite ok for small scale)
   - Set up static/media file serving (WhiteNoise or CDN)
   - Set DEBUG=False in settings.py
   - Set ALLOWED_HOSTS = ['yourdomain.com']

2. GOOGLE LOGIN (Production)
   - Google Cloud Console: add production domain to redirect URIs
   - Django admin: update Site domain to yourdomain.com

3. FORGOT PASSWORD (Production)
   - Change EMAIL_BACKEND to SMTP (e.g. SendGrid, Gmail SMTP)
   - Set EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

4. RAZORPAY (If needed later)
   - Uncomment Razorpay checkout JS in deposit.html
   - Wire create_order/payment_success views back
   - Get live keys from Razorpay dashboard

5. WHATSAPP NUMBER
   - Replace 919XXXXXXXXX with real number in base.html and contact.html

6. WITHDRAWAL (Automatic or Manual)
   - Currently: admin approves manually
   - For automatic: change zobet/views.py approve_withdrawal to auto-approve

7. SECURITY
   - Change SECRET_KEY to a strong random key
   - Use proper secret management (environment variables)

=== RUN COMMANDS ===
python manage.py runserver
python manage.py createsuperuser
python manage.py makemigrations
python manage.py migrate
