from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from . import views
from . import pages_views

handler404 = lambda request, exception: render(request, 'errors/404.html', status=404)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('terms/', pages_views.terms_view, name='terms'),
    path('privacy/', pages_views.privacy_view, name='privacy'),
    path('contact/', pages_views.contact_view, name='contact'),
    path('how-it-works/', pages_views.how_it_works_view, name='how_it_works'),
    path('faq/', pages_views.faq_view, name='faq'),
    path('about/', pages_views.about_view, name='about'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-dashboard/events/', views.admin_events_view, name='admin_events'),
    path('admin-dashboard/withdrawals/', views.admin_withdrawals_view, name='admin_withdrawals'),
    path('admin-dashboard/users/', views.admin_users_view, name='admin_users'),
    path('admin-dashboard/delete-event/<int:event_id>/', views.delete_event_view, name='delete_event'),
    path('admin-dashboard/approve-withdrawal/<int:withdrawal_id>/', views.approve_withdrawal_view, name='approve_withdrawal'),
    path('admin-dashboard/reject-withdrawal/<int:withdrawal_id>/', views.reject_withdrawal_view, name='reject_withdrawal'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('events/', include('events.urls')),
    path('wallet/', include('wallet.urls')),
    path('predictions/', include('predictions.urls')),
    path('payments/', include('payments.urls')),
    path('leaderboard/', include('leaderboard.urls')),
    path('notifications/', include('notifications.urls')),
    path('community/', include('community.urls')),
    path('dashboard/', include('accounts.urls_dashboard')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
