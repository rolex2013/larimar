import json
from datetime import datetime, date, time
from django.utils import timezone
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

#from channels_presence.decorators import remove_presence, touch_presence
#from channels_presence.signals import presence_changed
#from channels_presence.models import Room, Presence

#from django.dispatch import receiver
#from channels.layers import get_channel_layer

from django.contrib.auth.models import User
from chats.models import Chat, Message, ChatMember

#import logging


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['chatid']
        self.chat_member = self.scope['url_route']['kwargs']['memberid']
        #print('Открыт сокет chatid=', self.group_name, 'для userid=', self.chat_member, self.channel_name, self.scope)
        #print('Пользователь userid=', self.chat_member, 'вошёл в чат chatid=', self.group_name)
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        chat = Chat.objects.filter(id=self.group_name).first()
        # если тип чата - "Общий"
        if chat.type_id == 3:
            chatmember = ChatMember.objects.filter(chat_id=self.group_name, member_id=self.chat_member).first()
            if chatmember == None:
                #print(chatmember)
                ChatMember.objects.create(chat_id=self.group_name, member_id=self.chat_member, author_id=self.chat_member, dateonline=datetime.now(),
                                          datecurrent=datetime.now(), dateoffline=datetime.now())
            else:
                ChatMember.objects.filter(chat_id=self.group_name, member_id=self.chat_member).update(dateonline=datetime.now())
        else:
            ChatMember.objects.filter(chat_id=self.group_name, member_id=self.chat_member).update(dateonline=datetime.now())

        self.accept()

    def disconnect(self, close_code):
        #self.chat_name = self.scope['url_route']['kwargs']['chat_name']
        #self.chat_member = self.scope['url_route']['kwargs']['memberid']
        #print('Пользователь userid=', self.chat_member, 'покинул чат chatid=', self.group_name)
        ChatMember.objects.filter(chat_id=self.group_name, member_id=self.chat_member).update(dateoffline=datetime.now())
        #memb = ChatMember.objects.filter(chat_id=self.group_name, member_id=self.chat_member).first()
        #memb.dateoffline = datetime.now()
        #memb.save()
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    def receive(self, text_data):
        self.group_name = self.scope['url_route']['kwargs']['chatid']
        text_data_json = json.loads(text_data)
        chatid = text_data_json['chatid']
        userfromid = text_data_json['userfromid']
        userfromname = text_data_json['userfromname']
        ismemberslist = text_data_json['ismemberslist']
        formatDate = datetime.now().strftime("%d.%m.%y %H:%M:%S")

        if ismemberslist:
            # помещаем список участников чата в message
            #mess = []
            message = ''
            #ChatMember.objects.filter(chat_id=self.group_name, member_id=self.chat_member).update(datecurrent=datetime.now())
            memb = ChatMember.objects.filter(chat_id=self.group_name, member_id=self.chat_member).first()
            memb.datecurrent = datetime.now()
            memb.save()
            chatmembers = ChatMember.objects.filter(chat_id=self.group_name, is_active=True).order_by('-dateonline')
            #print(chatmembers)
            for mmb in chatmembers:
                dt = mmb.dateonline
                #dt = mmb.dateoffline
                #dt = mmb.datecurrent
                if dt is None:
                    #dt = mmb.dateonline
                    dt = mmb.dateonline
                    if dt is None:
                        dt = mmb.dateoffline
                ddt = ' '
                if not dt is None:
                    dt = dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
                    #dt = dt.split('+',1)[0]
                    ddt = str(dt.strftime("%d.%m.%y %H:%M:%S"))
                    #print(self.chat_member, dt)
                #if not dt is None:
                #    ddt = str(dt.strftime("%d.%m.%y %H:%M:%S"))
                #if mmb.is_online:
                #    dt = mmb.dateonline
                #    ddt = str(dt.strftime("%d.%m.%y %H:%M:%S"))
                elem_mmb = str(mmb.member_id) + '/' + str(mmb.is_online) + '/' + str(ddt) + '/' + str(mmb.member.username)
                message += str(elem_mmb) + ';'

                #print(dt, '/', str(dt.date())+' '+str(dt.time()), '/', dt.replace(tzinfo=timezone.utc).astimezone(tz=None), '/', ddt)
                #print('===:',mmb.dateonline,mmb.datecurrent,mmb.dateoffline,datetime.now(),mmb.is_online)
                #print(mmb.chat_id, mmb.member.username)

            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type": "notification_message",
                    "message": message,
                    #"message": [user.username for user in ChatMember.get_users()],
                    "chatid": chatid,
                    'userfromname': userfromname,
                    'date': formatDate,
                    'ismemberslist': ismemberslist
                },
            )
        else:
            message = text_data_json['message']
            print('Для чата chatid=', chatid, 'получено сообщение "' + message + '" (', formatDate, ')')
            Message.objects.create(chat_id=chatid, author_id=userfromid, text=message)
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type": "notification_message",
                    "message": message,
                    "chatid": chatid,
                    'userfromname': userfromname,
                    'date': formatDate,
                    'ismemberslist': ismemberslist
                },
            )

    # Receive message from room group
    def notification_message(self, event):
        message = event['message']
        chatid = event['chatid']
        userfromname = event['userfromname']
        ismemberslist = event['ismemberslist']
        #formatDate = date.today().strftime("%d.%m.%Y")
        formatDate = datetime.now().strftime("%d.%m.%y %H:%M:%S")
        print('В чат chatid=',chatid, 'отправлено сообщение "'+message+'" (',formatDate,')')
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            "chatid": chatid,
            'userfromname': userfromname,
            #'date': str(date.today())
            'date': formatDate,
            'ismemberslist': ismemberslist
        }))
