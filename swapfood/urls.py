from django.urls import path
from .views import search_users, MessageView

urlpatterns = [
    path('search_users/', search_users, name='search_users'),
    path('chat/<str:username>/', MessageView, name='chat_with_user'),
]
