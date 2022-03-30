import json
from datetime import datetime, date, time
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

from django.contrib.auth.models import User
from chats.models import Chat, Message, ChatMember


class ChatConsumer(WebsocketConsumer):
    #chat_name = self.scope['url_route']['kwargs']['chat_name']

    def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['chatid']
        self.chat_member = self.scope['url_route']['kwargs']['memberid']
        print('+++ chat +++', self.channel_name, self.group_name)
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        ChatMember.objects.filter(chat_id=self.group_name, member_id=self.chat_member).update(dateonline=datetime.now())
        self.accept()

    def disconnect(self, close_code):
        #self.chat_name = self.scope['url_route']['kwargs']['chat_name']
        self.chat_member = self.scope['url_route']['kwargs']['memberid']
        print('--- chat ---', self.channel_name, 'chatid=', self.group_name, 'webSocket закрыт!')
        ChatMember.objects.filter(chat_id=self.group_name, member_id=self.chat_member).update(dateoffline=datetime.now())
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    def receive(self, text_data):
        self.group_name = self.scope['url_route']['kwargs']['chatid']
        text_data_json = json.loads(text_data)
        chatid = text_data_json['chatid']
        userfromid = text_data_json['userfromid']
        userfromname = text_data_json['userfromname']
        message = text_data_json['message']
        #formatDate = datetime.now().strftime("%d.%m.%Y %H:%i:%s")
        formatDate = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        #recipient_user = User.objects.filter(id=userid).first()
        print(text_data, self.group_name, self.channel_name, 'chatid=', chatid, message, userfromname)
        Message.objects.create(chat_id=chatid, author_id=userfromid, text=message)
        #member = ChatMember.objects.filter(chat_id=self.group_name, member_id=self.chat_member)
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                "type": "notification_message",
                "message": message,
                "chatid": chatid,
                'userfromname': userfromname,
                #'member_isonline': member.is_online,
                #'recipient_user': recipient_user,
                #'date': str(date.today())
                'date': formatDate
            },
        )

    # Receive message from room group
    def notification_message(self, event):
        message = event['message']
        chatid = event['chatid']
        userfromname = event['userfromname']
        #formatDate = date.today().strftime("%d.%m.%Y")
        formatDate = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        #print(datetime.now(), formatDate)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            "chatid": chatid,
            'userfromname': userfromname,
            #'date': str(date.today())
            'date': formatDate
        }))
