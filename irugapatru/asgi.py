# mysite/asgi.py
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "irugapatru.settings")

import django
django.setup()

from django.core.management import call_command

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from game.routing import websocket_urlpatterns



# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "irugapatru.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

import game.routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)