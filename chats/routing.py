from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    #re_path(r'ws/chats/chat/(?P<chatid>\w+)/(?P<memberid>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chats/chat/(?P<chatid>\w+)/(?P<memberid>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chats/chat/member/(?P<chatid>\w+)/(?P<memberid>\w+)/$', consumers.ChatMemberConsumer.as_asgi()),
]