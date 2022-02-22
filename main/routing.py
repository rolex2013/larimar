from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    #re_path(r'ws/notification/(?P<chat_name>\w+)/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r'ws/main/notification/(?P<userid>\w+)/$', consumers.NotificationConsumer.as_asgi()),
]