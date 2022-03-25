import json
from datetime import datetime, date, time
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

from django.contrib.auth.models import User
from chats.models import Chat, Message


class ChatConsumer(WebsocketConsumer):
    #chat_name = self.scope['url_route']['kwargs']['chat_name']

    def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['chatid']
        print('+++ chat +++', self.channel_name, self.group_name)
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        #self.chat_name = self.scope['url_route']['kwargs']['chat_name']
        print('--- chat ---', self.channel_name, 'chatid=', self.group_name, 'webSocket закрыт!')
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    def receive(self, text_data):
        self.group_name = self.scope['url_route']['kwargs']['chatid']
        text_data_json = json.loads(text_data)
        chatid = text_data_json['chatid']
        userfromid = text_data_json['userfromid']
        userfromname = text_data_json['userfromname']
        message = text_data_json['message']
        #recipient_user = User.objects.filter(id=userid).first()
        print(text_data, self.group_name, self.channel_name, 'chatid=', chatid, message, userfromname)
        Message.objects.create(chat_id=chatid, author_id=userfromid, text=message)
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                "type": "notification_message",
                "message": message,
                "chatid": chatid,
                'userfromname': userfromname,
                #'recipient_user': recipient_user,
                'date': str(date.today())
            },
        )

    # Receive message from room group
    def notification_message(self, event):
        message = event['message']
        chatid = event['chatid']
        userfromname = event['userfromname']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            "chatid": chatid,
            'userfromname': userfromname,
            'date': str(date.today())
        }))
