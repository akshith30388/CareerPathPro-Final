import os

from django.core.asgi import get_asgi_application

environment = os.environ.get("ENVIRONMENT", "local").lower()
settings_module = "config.settings.production" if environment == "production" else "config.settings.local"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

django_asgi_app = get_asgi_application()

try:
    from channels.auth import AuthMiddlewareStack
    from channels.routing import ProtocolTypeRouter, URLRouter
    from routing import routing

    application = ProtocolTypeRouter(
        {
            "http": django_asgi_app,
            "websocket": AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns)),
        }
    )
except ImportError:
    application = django_asgi_app
