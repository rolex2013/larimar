import json
from datetime import datetime, date, time
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

from django.contrib.auth.models import User
from main.models import Notification


class NotificationConsumer(WebsocketConsumer):
    #chat_name = self.scope['url_route']['kwargs']['chat_name']

    def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['userid']
        print('Открыт сокет уведомлений для userid=', self.group_name, '(', self.channel_name, ')')
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        #self.chat_name = self.scope['url_route']['kwargs']['chat_name']
        print('Закрыт сокет уведомлений для userid=', self.group_name, '(', self.channel_name, ')')
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    def receive(self, text_data):
        self.group_name = self.scope['url_route']['kwargs']['userid']
        text_data_json = json.loads(text_data)
        userid = text_data_json['userid']
        userfromid = text_data_json['userfromid']
        userfromname = text_data_json['userfromname']
        message = text_data_json['message']
        user = User.objects.filter(id=userid).first()
        username = user.username
        userfrom = User.objects.filter(id=userfromid).first()
        userfromname = userfrom.username
        print(text_data, self.group_name, self.channel_name, 'userid=', userid, 'from=', userfromname, 'to=', username, message)
        print('Получено уведомление от author_id=', userfromid, 'recipient_id=', userid, 'text=', message)
        Notification.objects.create(type_id=3, author_id=userfromid, recipient_id=userid, objecttype_id=9, theme='Сообщение от ' + userfromname,
                                    text=message)
        #print("//////////////////", t_rounded)
        #dt = datetime.strftime(datetime.now(), '%d-%m-%y %H:%i:%s')
        formatDate = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                "type": "notification_message",
                "message": message,
                "userid": userid,
                "username": username,
                "userfromid": userfromid,
                "userfromname": userfromname,
                'date': formatDate
            },
        )

    # Receive message from room group
    def notification_message(self, event):
        #print('*-*-*-*-************ author_id=', event['userfromid'], 'recipient_id=', event['userid'], 'text=', event['message'])
        message = event['message']
        userid = event['userid']
        username = event['username']
        userfromid = event['userfromid']
        userfromname = event['userfromname']
        #usertoname = event['usertoname']
        #dt = datetime.strftime(datetime.now(), '%d-%m-%y %H:%i:%s')
        formatDate = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        #print("===================", t_rounded)

        #Notification.create(type_id=3, author_id=userfromid, recipient_id=userid, objecttype_id=9, text=message)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'userid': userid,
            'username': username,
            "userfromid": userfromid,
            "userfromname": userfromname,
            'date': formatDate
        }))

