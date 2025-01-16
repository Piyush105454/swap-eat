from django.urls import path
from swapfood.consumers import MychatApp

websocket_urlpatterns =[

    path('ws/wsc/',MychatApp.as_asgi())
]
