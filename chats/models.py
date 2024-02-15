from django.db import models

from datetime import datetime, timedelta
from django.utils import timezone

# from django.db import models
from django.urls import reverse, reverse_lazy
# from ckeditor_uploader.fields import RichTextUploadingField
from django_ckeditor_5.fields import CKEditor5Field

# from companies.models import Company

# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver

from django.utils.translation import gettext_lazy as _

# from main.utils_lang import TranslateFieldMixin
from main.utils_model import Dict_Model  # , Task_Model, Comment_Model

exposed_request = ""


class Dict_ChatType(Dict_Model):
    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    class Meta(Dict_Model.Meta):
        verbose_name = _("Тип чата")
        verbose_name_plural = _("Типы чатов")


class Chat(models.Model):
    name = models.CharField(_("Наименование"), max_length=128)
    description = models.CharField(_("Описание"), max_length=512)
    company = models.ForeignKey(
        "companies.Company",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="chats_company",
        verbose_name=_("Компания"),
    )
    type = models.ForeignKey(
        "Dict_ChatType",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="chats_chattype",
        verbose_name=_("Тип"),
    )
    datecreate = models.DateTimeField(_("Создан"), auto_now_add=True)
    dateclose = models.DateTimeField(
        _("Дата закрытия"), auto_now_add=False, blank=True, null=True
    )
    members = models.ManyToManyField(
        "auth.User",
        through="ChatMember",
        through_fields=("chat", "member"),
        related_name="chat_members",
        verbose_name=_("Участники"),
    )
    author = models.ForeignKey(
        "auth.User",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="chats_chat_author",
        verbose_name=_("Автор"),
    )
    is_active = models.BooleanField(_("Активность"), default=True)

    # def get_absolute_url(self):
    #    return reverse('my_chat:chat_detail', kwargs={'chatid': self.pk})
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Чат Компании")
        verbose_name_plural = _("Чаты компаний")


class ChatMember(models.Model):
    chat = models.ForeignKey(
        "Chat",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="chats_chatmember_chat",
        verbose_name=_("Чат"),
    )
    member = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="chats_chatmember_member",
        verbose_name=_("Участник"),
    )
    datecreate = models.DateTimeField(
        _("Создан"), auto_now_add=True
    )  # Момент вступления в чат
    dateclose = models.DateTimeField(
        _("Дата закрытия"), auto_now_add=False, blank=True, null=True
    )  # Момент выхода из члентства
    dateonline = models.DateTimeField(
        _("Момент входа в чат"), auto_now_add=False, blank=True, null=True
    )
    datecurrent = models.DateTimeField(
        _("Момент последней активности"), auto_now_add=False, blank=True, null=True
    )
    dateoffline = models.DateTimeField(
        _("Момент выхода из чата"), auto_now_add=False, blank=True, null=True
    )
    is_admin = models.BooleanField(_("Администратор"), default=False)
    author = models.ForeignKey(
        "auth.User",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="chats_chatmember_author",
        verbose_name=_("Автор"),
    )  # Пригласивший в чат
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def is_online(self):
        online = False
        if self.dateonline is not None:
            if not self.datecurrent:
                if timezone.now() - self.dateonline <= timedelta(milliseconds=30000):
                    online = True
            else:
                if timezone.now() - self.datecurrent <= timedelta(milliseconds=30000):
                    # if not self.dateoffline is None:
                    #    if (self.dateonline > self.dateoffline):
                    online = True
        return online

    def __str__(self):
        # return (self.chat__name + '. ' + self.member__username)
        return self.member.username
        # return (self.chat + '. ' + self.member)

    class Meta:
        verbose_name = _("Участник Чата")
        verbose_name_plural = _("Участники чатов")


# @receiver(post_save, sender=ChatMember)
# def post_save_member(sender, instance, **kwargs):
#    if kwargs['created']:
#        print(f'В чат "{instance.chat}" добавлен пользователь {instance}!')
#    else:
#        print(f'В чате "{instance.chat}" изменены данные пользователя {instance}!')


class Message(models.Model):
    # text = models.TextField("Наименование", max_length=2048)
    text = CKEditor5Field(_("Текст"), config_name="extends")
    chat = models.ForeignKey(
        "Chat",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="chats_chat",
        verbose_name=_("Чат"),
    )
    datecreate = models.DateTimeField(_("Создан"), auto_now_add=True)
    # dateclose = models.DateTimeField("Дата закрытия", auto_now_add=False, blank=True, null=True)
    onlyfor = models.ForeignKey(
        "auth.User",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="chats_message_onlyfor",
        verbose_name=_("Только для"),
    )
    author = models.ForeignKey(
        "auth.User",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="chats_message_autor",
        verbose_name=_("Автор"),
    )
    is_active = models.BooleanField(_("Активность"), default=True)

    # def get_absolute_url(self):
    #    return reverse('my_chat:chat_detail', kwargs={'chatid': self.chat.pk})
    def __str__(self):
        return str(self.author.username) + " (" + self.text + ") "

    class Meta:
        verbose_name = _("Сообщение пользователя")
        verbose_name_plural = _("Сообщения пользователей")
