
from django.urls import path, include

from . import views

app_name = 'my_chat'

urlpatterns = [

    path('chats_list/<int:companyid>/<int:chatid>/', views.chats, name='chats'),
    #path('chats_page/chat_create/<int:companyid>/', views.ChatCreate.as_view(), name='chat_create'),
    path('chats_page/chat_list/', views.chatslist, name='chats_list'),
    path('chats_page/chat_create/', views.chatcreate, name='chat_create'),
    #path('chats_page/message_list/<int:chatid>', views.messages, name='messages'),
    path('chats_page/message_list/', views.messages, name='messages'),
    path('chats_page/message_create/', views.messagecreate, name='message_create'),
    path('chats_page/message_form/', views.messageform, name='messageform'),
    path('chats_page/member_create/', views.membercreate, name='member_create'),
    path('chats_page/member_form/', views.memberform, name='memberform'),
    path('chats_page/member_list/', views.ajax_memberlist, name='ajax_memberlist'),
    #path('', views.notifications, name='notifications'),
    #path('chats_page/wschat/', views.wschat, name='wschat'),

]
