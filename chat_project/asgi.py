import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_project.settings')


from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()


import chat.routing
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

django.setup()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        )
    ),
})
