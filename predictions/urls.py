from django.urls import path
from . import views

app_name = 'predictions'

urlpatterns = [
    path('my/', views.my_predictions_view, name='my_predictions'),
    path('event/<int:event_id>/', views.event_predictions_view, name='event_predictions'),
]
