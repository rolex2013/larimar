from django.db import models

from django.db import models
from django.urls import reverse, reverse_lazy
from ckeditor_uploader.fields import RichTextUploadingField

from companies.models import Company

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
    chat = models.ForeignKey('Chat', limit_choices_to={'is_active': True},
                             on_delete=models.CASCADE, related_name='chats_chatmember_chat', verbose_name="Чат")
    member = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='chats_chatmember_member', verbose_name="Участник")
    datecreate = models.DateTimeField("Создан", auto_now_add=True)                                                                                         # Момент вступления в чат
    dateclose = models.DateTimeField("Дата закрытия", auto_now_add=False, blank=True, null=True)                                                           # Момент выхода из члентства
    author = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.CASCADE, related_name='chats_chatmember_author', verbose_name="Автор") # Пригласивший в чат
    is_active = models.BooleanField("Активность", default=True)

    def __str__(self):
        return (self.chat__name + '. ' + self.member__username)
        #return (self.chat + '. ' + self.member)
    class Meta:
        verbose_name = 'Участник Чата'
        verbose_name_plural = 'Участники чатов'

class Message(models.Model):
    text = models.TextField("Наименование", max_length=2048)
    chat = models.ForeignKey('Chat', limit_choices_to={'is_active': True},
                             on_delete=models.CASCADE, related_name='chats_chat', verbose_name="Чат")
    datecreate = models.DateTimeField("Создан", auto_now_add=True)
    #dateclose = models.DateTimeField("Дата закрытия", auto_now_add=False, blank=True, null=True)
    author = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.CASCADE, related_name='chats_message_autor', verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True)

    #def get_absolute_url(self):
    #    return reverse('my_chat:chat_detail', kwargs={'chatid': self.chat.pk})
    def __str__(self):
        return (self.author + " (" + self.text + ") " + self.name)
    class Meta:
        verbose_name = 'Сообщение пользователя'
        verbose_name_plural = 'Сообщения пользователей'