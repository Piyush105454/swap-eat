from django.urls import path
from swapfood.consumers import PrivateChatConsumer

websocket_urlpatterns = [
    path("ws/chat/<str:username>/", PrivateChatConsumer.as_asgi()),
]
