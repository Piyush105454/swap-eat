import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from swapfood.routing import websocket_urlpatterns  # Ensure this import path is correct

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swapeat.settings')

# Initialize Django ASGI application early to ensure the apps are loaded
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
