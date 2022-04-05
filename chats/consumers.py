import json
from datetime import datetime, date, time
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

from channels_presence.decorators import remove_presence, touch_presence
from channels_presence.models import Room, Presence

from django.contrib.auth.models import User
from chats.models import Chat, Message, ChatMember


class ChatConsumer(WebsocketConsumer):
    #chat_name = self.scope['url_route']['kwargs']['chat_name']

    def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['chatid']
        self.chat_member = self.scope['url_route']['kwargs']['memberid']
        #print('Открыт сокет chatid=', self.group_name, 'для userid=', self.chat_member, self.channel_name, self.scope)
        print('Пользователь userid=', self.chat_member, 'вошёл в чат chatid=', self.group_name)
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        #ChatMember.objects.filter(chat_id=self.group_name, member_id=self.chat_member).update(dateonline=datetime.now())
        memb = ChatMember.objects.filter(chat_id=self.group_name, member_id=self.chat_member).first()
        memb.dateonline = datetime.now()
        memb.save()
        Room.objects.add(self.group_name, self.channel_name, self.scope["user"])
        self.accept()
        #self.send(text_data=json.dumps({'nodes_members': ChatMember.objects.filter(chat=self.group_name,
        #                                           is_active=True,
        #                                           dateclose__isnull=True).select_related("member", "author").order_by('-is_admin', '-dateonline')}))

    @remove_presence
    def disconnect(self, close_code):
        #self.chat_name = self.scope['url_route']['kwargs']['chat_name']
        self.chat_member = self.scope['url_route']['kwargs']['memberid']
        #print('Закрыт сокет chatid=', self.group_name, self.channel_name, self.scope, self.scope["user"])
        print('Пользователь userid=', self.chat_member, 'покинул чат chatid=', self.group_name)
        #ChatMember.objects.filter(chat_id=self.group_name, member_id=self.chat_member).update(dateoffline=datetime.now())
        memb = ChatMember.objects.filter(chat_id=self.group_name, member_id=self.chat_member).first()
        memb.dateoffline = datetime.now()
        memb.save()
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        #self.send(text_data=json.dumps({'nodes_members': ChatMember.objects.filter(chat=self.group_name,
        #                                           is_active=True,
        #                                           dateclose__isnull=True).select_related("member", "author").order_by('-is_admin', '-dateonline')}))
        #self.send(text_data=json.dumps({'scope': self.scope}))
        formatDate = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
             "type": "forward.message",
               #self.send(text_data=json.dumps({
            'message': 'Userid=' + str(self.chat_member) + ' вышел из чата!',
            "chatid": self.group_name,
            'userfromname': self.scope["user"],
            'date': formatDate
        })
        #logger.error("Token doesn't exist while closing the connection")


    @touch_presence
    def receive(self, text_data):
        self.group_name = self.scope['url_route']['kwargs']['chatid']
        text_data_json = json.loads(text_data)
        chatid = text_data_json['chatid']
        userfromid = text_data_json['userfromid']
        userfromname = text_data_json['userfromname']
        message = text_data_json['message']
        formatDate = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        #recipient_user = User.objects.filter(id=userid).first()
        print(text_data, self.group_name, self.channel_name, 'chatid=', chatid, message, userfromname)
        Message.objects.create(chat_id=chatid, author_id=userfromid, text=message)
        #member = ChatMember.objects.filter(chat_id=self.group_name, member_id=self.chat_member)
        if text_data == '"heartbeat"':
            Presence.objects.touch(self.channel_name)
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
        print('$$$$$$$$$$$$$$', datetime.now(), formatDate, message)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            "chatid": chatid,
            'userfromname': userfromname,
            #'date': str(date.today())
            'date': formatDate
        }))

    #def forward_message(self, event):
    #    """
    #    Utility handler for messages to be broadcasted to groups.  Will be
    #    called from channel layer messages with `"type": "forward.message"`.
    #    """
    #    print('event: ', event["message"])
    #    self.send(event["message"])
