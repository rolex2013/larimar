from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chats/chat/(?P<chatid>\w+)/$', consumers.ChatConsumer.as_asgi()),
]