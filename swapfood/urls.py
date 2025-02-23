from django.urls import path
from . import views

urlpatterns = [
    # Open chat page where user can enter a username to start chatting
    path('chat/', views.chat, name='chat'),

    # Route to open messages with username input
    path('chat/<str:room_name>/<str:username>/', views.MessageView, name='chat_with_user'),

    # Search users
    path('search_users/', views.search_users, name='search_users'),

    # Other URLs...
]
