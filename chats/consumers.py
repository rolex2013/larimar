import json
from datetime import datetime, date, time
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync



class NotificationConsumer(WebsocketConsumer):
    #chat_name = self.scope['url_route']['kwargs']['chat_name']

    def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['userid']
        print('+++', self.channel_name, self.group_name)
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        #self.chat_name = self.scope['url_route']['kwargs']['chat_name']
        print('---', self.channel_name, self.group_name)
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    def receive(self, text_data):
        self.group_name = self.scope['url_route']['kwargs']['userid']
        text_data_json = json.loads(text_data)
        userid = text_data_json['userid']
        message = text_data_json['message']
        print(text_data, self.group_name, self.channel_name, 'userid=', userid, message)
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                "type": "notification_message",
                "message": message,
                "userid": userid,
                'date': str(date.today())
            },
        )

    # Receive message from room group
    def notification_message(self, event):
        message = event['message']
        userid = event['userid']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            "userid": userid,
            'date': str(date.today())
        }))
