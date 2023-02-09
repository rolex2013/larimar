from django.db import models

from datetime import datetime, timedelta
from django.utils import timezone

from django.db import models
from django.urls import reverse, reverse_lazy
from ckeditor_uploader.fields import RichTextUploadingField

from companies.models import Company

#from django.db.models.signals import post_save, pre_save
#from django.dispatch import receiver

class Dict_ChatType(models.Model):
    name = models.CharField("Наименование", max_length=64)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Тип чата'
        verbose_name_plural = 'Типы чатов'
    def __str__(self):
        return (self.name)

class Chat(models.Model):
    name = models.CharField("Наименование", max_length=128)
    description = models.CharField("Описание", max_length=512)
    company = models.ForeignKey('companies.Company', null=True, blank=True, on_delete=models.CASCADE, related_name='chats_company',
                                verbose_name="Компания")
    type = models.ForeignKey('Dict_ChatType', limit_choices_to={'is_active': True},
                               on_delete=models.CASCADE, related_name='chats_chattype', verbose_name="Тип")
    datecreate = models.DateTimeField("Создан", auto_now_add=True)
    dateclose = models.DateTimeField("Дата закрытия", auto_now_add=False, blank=True, null=True)
    members = models.ManyToManyField('auth.User', through="ChatMember", through_fields=('chat', 'member'), related_name='chat_members', verbose_name="Участники")
    author = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.CASCADE, related_name='chats_chat_author', verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True)

    #def get_absolute_url(self):
    #    return reverse('my_chat:chat_detail', kwargs={'chatid': self.pk})
    def __str__(self):
        return (self.name)
    class Meta:
        verbose_name = 'Чат Компании'
        verbose_name_plural = 'Чаты компаний'

class ChatMember(models.Model):
    chat = models.ForeignKey('Chat', limit_choices_to={'is_active': True}, on_delete=models.CASCADE, related_name='chats_chatmember_chat', verbose_name="Чат")
    member = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='chats_chatmember_member', verbose_name="Участник")
    datecreate = models.DateTimeField("Создан", auto_now_add=True)                                                                                         # Момент вступления в чат
    dateclose = models.DateTimeField("Дата закрытия", auto_now_add=False, blank=True, null=True)                                                           # Момент выхода из члентства
    dateonline = models.DateTimeField("Момент входа в чат", auto_now_add=False, blank=True, null=True)
    datecurrent = models.DateTimeField("Момент последней активности", auto_now_add=False, blank=True, null=True)
    dateoffline = models.DateTimeField("Момент выхода из чата", auto_now_add=False, blank=True, null=True)
    is_admin = models.BooleanField("Администратор", default=False)
    author = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.CASCADE, related_name='chats_chatmember_author', verbose_name="Автор") # Пригласивший в чат
    is_active = models.BooleanField("Активность", default=True)

    @property
    def is_online(self):
        online = False
        if not self.dateonline is None:
            if not self.datecurrent:
                if (timezone.now()-self.dateonline <= timedelta(milliseconds=30000)):
                    online = True
            else:
                if (timezone.now() - self.datecurrent <= timedelta(milliseconds=30000)):
                #if not self.dateoffline is None:
                #    if (self.dateonline > self.dateoffline):
                    online = True
        return online

    def __str__(self):
        #return (self.chat__name + '. ' + self.member__username)
        return (self.member.username)
        #return (self.chat + '. ' + self.member)
    class Meta:
        verbose_name = 'Участник Чата'
        verbose_name_plural = 'Участники чатов'

#@receiver(post_save, sender=ChatMember)
#def post_save_member(sender, instance, **kwargs):
#    if kwargs['created']:
#        print(f'В чат "{instance.chat}" добавлен пользователь {instance}!')
#    else:
#        print(f'В чате "{instance.chat}" изменены данные пользователя {instance}!')


class Message(models.Model):
    #text = models.TextField("Наименование", max_length=2048)
    text = RichTextUploadingField("Текст")
    chat = models.ForeignKey('Chat', limit_choices_to={'is_active': True},
                             on_delete=models.CASCADE, related_name='chats_chat', verbose_name="Чат")
    datecreate = models.DateTimeField("Создан", auto_now_add=True)
    #dateclose = models.DateTimeField("Дата закрытия", auto_now_add=False, blank=True, null=True)
    onlyfor = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.CASCADE, related_name='chats_message_onlyfor', verbose_name="Только для")
    author = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.CASCADE, related_name='chats_message_autor', verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True)

    #def get_absolute_url(self):
    #    return reverse('my_chat:chat_detail', kwargs={'chatid': self.chat.pk})
    def __str__(self):
        return (str(self.author.username) + " (" + self.text + ") ")
    class Meta:
        verbose_name = 'Сообщение пользователя'
        verbose_name_plural = 'Сообщения пользователей'