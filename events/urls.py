from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list_view, name='list'),
    path('<int:event_id>/', views.event_detail_view, name='detail'),
    path('<int:event_id>/predict/<int:team_id>/', views.predict_view, name='predict'),
    path('<int:event_id>/declare-winner/', views.declare_winner_view, name='declare_winner'),
    path('create/', views.create_event_view, name='create_event'),
    path('<int:event_id>/edit/', views.edit_event_view, name='edit_event'),
    path('<int:event_id>/add-teams/', views.add_teams_view, name='add_teams'),
]
