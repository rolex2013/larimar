from django.db import models

from django.urls import reverse

# from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey

from ckeditor_uploader.fields import RichTextUploadingField

from main.models import ModelLog
from companies.models import Company

from dashboard.utils import SetPropertiesDashboardMixin

# import json
from datetime import datetime

from django.utils.translation import gettext_lazy as _
from main.utils_lang import TranslateFieldMixin
from main.utils_model import Dict_Model, Comment_Model

exposed_request = ""


class Dict_ClientType(TranslateFieldMixin, models.Model):
    name_ru = models.CharField(_("Наименование_ru"), max_length=64)
    name_en = models.CharField(_("Наименование_en"), max_length=64)
    description_ru = models.TextField(_("Описание_ru"), blank=True, null=True)
    description_en = models.TextField(_("Описание_en"), blank=True, null=True)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    class Meta:
        ordering = ("sort",)
        verbose_name = _("Тип клиента")
        verbose_name_plural = _("Типы клиентов")

    def __str__(self):
        return self.name


class Dict_ClientStatus(TranslateFieldMixin, models.Model):
    name_ru = models.CharField(_("Наименование_ru"), max_length=64)
    name_en = models.CharField(_("Наименование_en"), max_length=64)
    description_ru = models.TextField(_("Описание_ru"), blank=True, null=True)
    description_en = models.TextField(_("Описание_en"), blank=True, null=True)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    is_close = models.BooleanField(_("Закрывает клиента"), default=False)
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    class Meta:
        ordering = ("sort",)
        verbose_name = _("Статус клиента")
        verbose_name_plural = _("Статусы клиентов")

    def __str__(self):
        return self.name


class Dict_ClientTaskStatus(TranslateFieldMixin, models.Model):
    name_ru = models.CharField(_("Наименование_ru"), max_length=64)
    name_en = models.CharField(_("Наименование_en"), max_length=64)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    is_close = models.BooleanField(_("Закрывает задачу"), default=False)
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    class Meta:
        ordering = ("sort",)
        verbose_name = _("Статус задачи")
        verbose_name_plural = _("Статусы задач")

    def __str__(self):
        return self.name


class Dict_ClientTaskStructureType(TranslateFieldMixin, models.Model):
    name_ru = models.CharField(_("Наименование_ru"), max_length=64)
    name_en = models.CharField(_("Наименование_en"), max_length=64)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    class Meta:
        ordering = ("sort",)
        verbose_name = _("Тип задачи в иерархии")
        verbose_name_plural = _("Типы задач в иерархии")

    def __str__(self):
        return self.name


class Dict_ClientTaskType(TranslateFieldMixin, models.Model):
    name_ru = models.CharField(_("Наименование_ru"), max_length=64)
    name_en = models.CharField(_("Наименование_en"), max_length=64)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    class Meta:
        ordering = ("sort",)
        verbose_name = _("Тип задачи")
        verbose_name_plural = _("Типы задач")

    def __str__(self):
        return self.name


class Dict_ClientEventType(TranslateFieldMixin, models.Model):
    name_ru = models.CharField(_("Наименование_ru"), max_length=64)
    name_en = models.CharField(_("Наименование_en"), max_length=64)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    class Meta:
        ordering = ("sort",)
        verbose_name = _("Тип события")
        verbose_name_plural = _("Типы событий")

    def __str__(self):
        return self.name


class Dict_ClientEventStatus(TranslateFieldMixin, models.Model):
    name_ru = models.CharField(_("Наименование_ru"), max_length=64)
    name_en = models.CharField(_("Наименование_en"), max_length=64)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    is_close = models.BooleanField(_("Закрывает событие"), default=False)
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    class Meta:
        ordering = ("sort",)
        verbose_name = _("Статус события")
        verbose_name_plural = _("Статусы событий")

    def __str__(self):
        return self.name


class Dict_ClientInitiator(TranslateFieldMixin, models.Model):
    name_ru = models.CharField(_("Наименование_ru"), max_length=64)
    name_en = models.CharField(_("Наименование_en"), max_length=64)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    class Meta:
        ordering = ("sort",)
        verbose_name = _("Инициатор")
        verbose_name_plural = _("Инициаторы")

    def __str__(self):
        return self.name


class Client(models.Model):
    # WHO_INIT = (('CLNT', 'Клиент'), ('ORG', 'Компания'), ('OTHER', 'Другое'))
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="result_company_client",
        verbose_name=_("Организация"),
    )
    manager = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="result_manager_client",
        verbose_name=_("Менеджер"),
    )
    user = models.OneToOneField(
        "auth.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="result_user_client",
        verbose_name=_("Пользователь"),
    )
    is_notify = models.BooleanField(_("Оповещать"), default=False)
    protocoltype = models.ForeignKey(
        "main.Dict_ProtocolType",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="result_protocoltype_client",
        verbose_name=_("Протокол оповещения"),
    )
    type = models.ForeignKey(
        "Dict_ClientType",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="client_type_client",
        verbose_name=_("Тип клиента"),
    )
    status = models.ForeignKey(
        "Dict_ClientStatus",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="client_status_client",
        verbose_name=_("Статус клиента"),
    )
    firstname = models.CharField(_("Имя"), max_length=64)
    middlename = models.CharField(_("Отчество"), blank=True, null=True, max_length=64)
    lastname = models.CharField(_("Фамилия"), max_length=64)
    email = models.CharField("E-mail", max_length=64, blank=True, null=True)
    phone = models.CharField(_("Телефон"), max_length=16, blank=True, null=True)
    # description = models.TextField(_("Описание")
    description = RichTextUploadingField(_("Описание"), blank=True, null=True)
    currency = models.ForeignKey(
        "finance.Dict_Currency",
        on_delete=models.CASCADE,
        related_name="result_currency_client",
        verbose_name=_("Валюта"),
    )
    cost = models.DecimalField(
        _("Стоимость"), max_digits=12, decimal_places=2, default=0
    )
    percentage = models.DecimalField(
        _("Процент выполнения"), max_digits=5, decimal_places=2, default=0
    )
    datecreate = models.DateTimeField(_("Создан"), auto_now_add=True)
    dateclose = models.DateTimeField(
        _("Дата закрытия"), auto_now_add=False, blank=True, null=True
    )
    # initiator = models.CharField(_("Инициатор"), max_length = 5, choices=WHO_INIT)
    initiator = models.ForeignKey(
        "Dict_ClientInitiator",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="client_initiator_client",
        verbose_name=_("Инициатор клиента"),
    )
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="client_author",
        verbose_name=_("Автор"),
    )
    members = models.ManyToManyField(
        "auth.User", related_name="client_members", verbose_name=_("Участники")
    )
    is_active = models.BooleanField(_("Активность"), default=True)

    def get_absolute_url(self):
        # return reverse('my_crm:client_detail', kwargs={'userid': self.user.pk, 'param': ' '})
        return reverse("my_crm:clienttasks", kwargs={"clientid": self.pk, "pk": "0"})
        # return reverse('my_crm:clients0')

    def __str__(self):
        # return (self.user.username + ' - ' + self.company.name)
        # return (self.user.username)
        return self.firstname + " " + self.middlename + " " + self.lastname

    class Meta:
        # unique_together = ('user','company')
        # ordering = ('user')
        verbose_name = _("Клиент")
        verbose_name_plural = _("Клиенты")


class ClientTask(SetPropertiesDashboardMixin, MPTTModel):
    name = models.CharField(_("Наименование"), max_length=128)
    description = RichTextUploadingField(_("Описание"), null=True, blank=True)
    datebegin = models.DateTimeField(_("Начало"))
    dateend = models.DateTimeField(_("Окончание"))
    client = models.ForeignKey(
        "Client",
        on_delete=models.CASCADE,
        related_name="resultclient",
        verbose_name=_("Клиент"),
    )
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="task_children",
        verbose_name=_("Задача верхнего уровня"),
    )
    assigner = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="clienttask_assigner",
        verbose_name=_("Исполнитель"),
    )
    cost = models.DecimalField(_("Стоимость"), max_digits=12, decimal_places=2)
    percentage = models.DecimalField(
        _("Процент выполнения"), max_digits=5, decimal_places=2, default=0
    )
    structure_type = models.ForeignKey(
        "Dict_ClientTaskStructureType",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="clienttask_structure_type",
        verbose_name=_("Тип в иерархии"),
    )
    type = models.ForeignKey(
        "Dict_ClientTaskType",
        null=True,
        blank=True,
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="clienttask_type",
        verbose_name=_("Тип"),
    )
    # typeevent = models.ForeignKey('Dict_ClientEventType', null=True, blank=True, limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='clientevent_type', verbose_name=_("Тип события"))
    status = models.ForeignKey(
        "Dict_ClientTaskStatus",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="clienttask_status",
        verbose_name=_("Статус"),
    )
    datecreate = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    dateclose = models.DateTimeField(
        _("Дата закрытия"), auto_now_add=False, blank=True, null=True
    )
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="resultclienttaskuser",
        verbose_name="Автор",
    )
    initiator = models.ForeignKey(
        "Dict_ClientInitiator",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="clienttask_initiator",
        verbose_name=_("Инициатор"),
    )
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def object_name(self):
        return ("crm_tsk", _("Задача клиента"))

    def get_absolute_url(self):
        return reverse("my_crm:clienttaskcomments", kwargs={"taskid": self.pk})
        # return reverse('my_crm:clienttaskcomments, kwargs={'taskid': self.pk})

    def __str__(self):
        return (
            str(self.client)
            + ". "
            + self.name
            + " ("
            + self.datebegin.strftime("%d.%m.%Y, %H:%M")
            + " - "
            + self.dateend.strftime("%d.%m.%Y, %H:%M")
            + ")"
        )

    class MPTTMeta:
        # order_insertion_by = ['name']
        order_insertion_by = ["-dateend"]

    class Meta:
        verbose_name = _("Задача")
        verbose_name_plural = _("Задачи")


class ClientTaskComment(Comment_Model):
    task = models.ForeignKey(
        "ClientTask",
        on_delete=models.CASCADE,
        related_name="resultclienttask",
        verbose_name=_("Задача"),
    )

    def get_absolute_url(self):
        return reverse("my_crm:clienttaskcomments", kwargs={"taskid": self.task_id})

    @property
    def files(self):
        return ClientFile.objects.filter(taskcomment_id=self.id, is_active=True)

    class Meta:
        verbose_name = _("Комментарий")
        verbose_name_plural = _("Комментарии")


class ClientEvent(SetPropertiesDashboardMixin, models.Model):
    name = models.CharField(_("Наименование"), max_length=128)
    description = RichTextUploadingField(_("Описание"), null=True, blank=True)
    datebegin = models.DateTimeField(_("Начало"))
    dateend = models.DateTimeField(_("Окончание"))
    place = models.CharField(_("Место"), max_length=254, null=True, blank=True)
    client = models.ForeignKey(
        "Client",
        on_delete=models.CASCADE,
        related_name="event_client",
        verbose_name=_("Клиент"),
    )
    task = models.ForeignKey(
        "ClientTask",
        null=True,
        blank=True,
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="eventtask",
        verbose_name=_("Связанная задача"),
    )
    assigner = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="event_assigner",
        verbose_name=_("Исполнитель"),
    )
    type = models.ForeignKey(
        "Dict_ClientEventType",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="event_type",
        verbose_name=_("Тип события"),
    )
    status = models.ForeignKey(
        "Dict_ClientEventStatus",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="event_status",
        verbose_name=_("Статус события"),
    )
    datecreate = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    dateclose = models.DateTimeField(
        _("Дата закрытия"), auto_now_add=False, blank=True, null=True
    )
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="event_user",
        verbose_name=_("Автор"),
    )
    initiator = models.ForeignKey(
        "Dict_ClientInitiator",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="event_initiator",
        verbose_name=_("Инициатор"),
    )
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def object_name(self):
        return ("crm_evnt", _("Событие клиента"))

    def get_absolute_url(self):
        return reverse("my_crm:clienteventcomments", kwargs={"eventid": self.pk})

    def __str__(self):
        return (
            str(self.client)
            + ". "
            + self.name
            + " ("
            + self.datebegin.strftime("%d.%m.%Y, %H:%M")
            + " - "
            + self.dateend.strftime("%d.%m.%Y, %H:%M")
            + ")"
        )

    class MPTTMeta:
        # order_insertion_by = ['name']
        order_insertion_by = ["-dateend"]

    class Meta:
        verbose_name = _("Событие")
        verbose_name_plural = _("События")


class ClientEventComment(Comment_Model):
    event = models.ForeignKey(
        "ClientEvent",
        on_delete=models.CASCADE,
        related_name="resultclientevent",
        verbose_name=_("Событие"),
    )
    time = models.DecimalField(
        _("Затраченное время, час."),
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    cost = models.DecimalField(
        _("Стоимость"),
        max_digits=9,
        decimal_places=2,
        blank=True,
        null=True,
        default=0
    )

    def get_absolute_url(self):
        return reverse("my_crm:clienteventcomments", kwargs={"eventid": self.event_id})

    def __str__(self):
        return (
            str(self.event)
            + ". "
            + self.name
            + " ("
            + self.datecreate.strftime("%d.%m.%Y, %H:%M")
            + ")"
        )

    @property
    def files(self):
        return ClientFile.objects.filter(eventcomment_id=self.id, is_active=True)

    class Meta:
        verbose_name = _("Комментарий")
        verbose_name_plural = _("Комментарии")


class ClientFile(models.Model):
    name = models.CharField(_("Наименование"), null=True, blank=True, max_length=255)
    uname = models.CharField(
        _("Уникальное наименование"), null=True, blank=True, max_length=255
    )
    client = models.ForeignKey(
        "Client",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="client_file",
        verbose_name=_("Клиент"),
    )
    task = models.ForeignKey(
        "ClientTask",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="clienttask_file",
        verbose_name=_("Задача"),
    )
    taskcomment = models.ForeignKey(
        "ClientTaskComment",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="clienttaskcomment_file",
        verbose_name=_("Комментарий"),
    )
    event = models.ForeignKey(
        "ClientEvent",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="clientevent_file",
        verbose_name="Событие",
    )
    eventcomment = models.ForeignKey(
        "ClientEventComment",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="clienteventcomment_file",
        verbose_name=_("Комментарий события"),
    )
    pfile = models.FileField(
        upload_to="uploads/files/crm", blank=True, null=True, verbose_name="Файл"
    )
    psize = models.PositiveIntegerField(editable=False, null=True, blank=True)
    datecreate = models.DateTimeField(_("Создан"), auto_now_add=True)
    author = models.ForeignKey(
        "auth.User",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("Автор"),
    )
    is_active = models.BooleanField(_("Активность"), default=True)

    class Meta:
        verbose_name = _("Файлы")
        verbose_name_plural = _("Файлы")

    def __str__(self):
        return str(self.id) + " " + self.uname  # file.name
