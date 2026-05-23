from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('create-order/', views.create_order_view, name='create_order'),
    path('webhook/', views.payment_webhook_view, name='webhook'),
    path('success/', views.payment_success_view, name='success'),
]
