"""
ASGI config for larimar project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

import main.routing
import chats.routing


#import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "larimar.settings")
from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
    #'http': AsgiHandler(),
    #"http": get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(AuthMiddlewareStack(
        URLRouter(
            main.routing.websocket_urlpatterns +
            chats.routing.websocket_urlpatterns
        )
    )),
})
