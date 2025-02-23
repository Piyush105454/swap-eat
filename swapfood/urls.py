from . import views
from django.urls import path

urlpatterns = [
    # Route to open the chat page (messages.html)
    path('chat/', views.chat, name='chat'),

    # Route to open messages with username input
    path('chat/<str:room_name>/<str:username>/', views.MessageView, name='room'),
    
]
