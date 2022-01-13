
from django.urls import path, include

from . import views

app_name = 'my_chat'

urlpatterns = [

    path('chats_list/<int:companyid>/', views.chats, name='chats'),
    path('chats_page/chat_create/<int:companyid>/', views.ChatCreate.as_view(), name='chat_create'),
    path('chats_page/message_list/<int:chatid>', views.messages, name='messages'),
    path('chats_page/message_create/<int:chatid>', views.MessageCreate.as_view(), name='message_create'),

]
