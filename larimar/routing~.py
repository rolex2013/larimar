
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
#from channels.security.websocket import AllowedHostsOriginValidator
import chats.routing

application = ProtocolTypeRouter({
    #'http': AsgiHandler(),
    #'websocket': AllowedHostsOriginValidator(AuthMiddlewareStack(
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chats.routing.websocket_urlpatterns
        )
    ),
})
