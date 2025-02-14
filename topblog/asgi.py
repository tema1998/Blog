import os

import django
from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "topblog.settings")
django.setup()
django_asgi_app = get_asgi_application()

import chat.routing
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from chat import consumers
from django.urls import path


if bool(int(os.getenv("DJANGO_DEVELOPMENT", 1))):
    application = ProtocolTypeRouter(
        {
            "http": django_asgi_app,
            "websocket": AllowedHostsOriginValidator(
                AuthMiddlewareStack(
                    URLRouter(chat.routing.websocket_urlpatterns)
                )
            ),
        }
    )
else:
    application = ProtocolTypeRouter(
        {
            "http": get_asgi_application(),
            "websocket": AuthMiddlewareStack(
                URLRouter(chat.routing.websocket_urlpatterns)
            ),
        }
    )
