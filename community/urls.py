from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.community_chat, name='chat'),
    path('api/messages/', views.chat_messages_api, name='chat_api'),
]
