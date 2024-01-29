from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from datetime import datetime

from mptt.models import MPTTModel, TreeForeignKey
from main.models import ModelLog
from companies.models import Company

from dashboard.utils import SetPropertiesDashboardMixin
from main.utils_lang import TranslateFieldMixin
from main.utils_model import Dict_Model, Comment_Model

from ckeditor_uploader.fields import RichTextUploadingField


exposed_request = ""


class Dict_System(models.Model):
    code = models.CharField(_("Код системы"), editable=False, max_length=128)
    name = models.CharField(_("Наименование системы"), max_length=128)
    # name_ru = models.CharField(_("Наименование системы _ru"), max_length=128)
    # name_en = models.CharField(
    #     _("Наименование системы _en"), max_length=128, blank=True, null=True
    # )
    domain = models.CharField(
        _("Наименование домена"), max_length=64, blank=True, null=True
    )
    url = models.CharField(_("url"), max_length=128)
    ip = models.CharField(_("ip-адрес"), max_length=15, blank=True, null=True)
    email = models.CharField(
        _("Контактный e-mail"), max_length=64, blank=True, null=True
    )
    phone = models.CharField(
        _("Контактный телефон"), max_length=15, blank=True, null=True
    )
    datecreate = models.DateTimeField(_("Создана"), auto_now_add=True)
    dateclose = models.DateTimeField(
        _("Дата закрытия"), auto_now_add=False, blank=True, null=True
    )
    requeststatuscode = models.IntegerField(
        _("Код завершения операции"), blank=True, null=True
    )
    is_local = models.BooleanField(_("Локальность"), default=True)
    is_active = models.BooleanField(_("Активность"), default=True)

    # @property
    # def name(self):
    #     return self.trans_field(exposed_request, "name")

    class Meta:
        # ordering = ('sort',)
        verbose_name = _("Система")
        verbose_name_plural = _("Системы")

    def __str__(self):
        return self.name + ". " + self.code + ". " + self.domain

    def get_absolute_url(self):
        return reverse(
            "my_feedback:tickets0",
            kwargs={"is_ticketslist_dev": 1, "systemid": self.pk},
        )


class Dict_FeedbackTicketStatus(TranslateFieldMixin, models.Model):
    name_ru = models.CharField(_("Наименование_ru"), max_length=64)
    name_en = models.CharField(
        _("Наименование_en"), max_length=64, blank=True, null=True
    )
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    is_close = models.BooleanField(_("Закрывает тикет"), default=False)
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    class Meta:
        ordering = ("sort",)
        verbose_name = _("Статус тикета")
        verbose_name_plural = _("Статусы тикетов")

    def __str__(self):
        return self.name


class Dict_FeedbackTicketType(TranslateFieldMixin, models.Model):
    name_ru = models.CharField(_("Наименование_ru"), max_length=64)
    name_en = models.CharField(
        _("Наименование_en"), max_length=64, blank=True, null=True
    )
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    class Meta:
        ordering = ("sort",)
        verbose_name = _("Тип тикета")
        verbose_name_plural = _("Типы тикетов")

    def __str__(self):
        return self.name


class Dict_FeedbackTaskStatus(TranslateFieldMixin, models.Model):
    name_ru = models.CharField(_("Наименование_ru"), max_length=64)
    name_en = models.CharField(
        _("Наименование_en"), max_length=64, blank=True, null=True
    )
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


class FeedbackTicket(SetPropertiesDashboardMixin, models.Model):
    system = models.ForeignKey(
        "Dict_System",
        on_delete=models.CASCADE,
        related_name="feedback_system",
        verbose_name=_("Система"),
    )
    company = models.ForeignKey(
        "companies.Company",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="feedback_company",
        verbose_name=_("Компания"),
    )
    companyfrom = models.ForeignKey(
        "companies.Company",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="feedback_companyfrom",
        verbose_name=_("Компания автора"),
    )
    # id_local = models.PositiveIntegerField("Локальный ID")
    name = models.CharField(_("Наименование"), max_length=128)
    description = RichTextUploadingField(_("Описание"))
    type = models.ForeignKey(
        "Dict_FeedbackTicketType",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="feedback_tickettype",
        verbose_name=_("Тип"),
    )
    status = models.ForeignKey(
        "Dict_FeedbackTicketStatus",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="feedback_ticketstatus",
        verbose_name=_("Статус"),
    )
    datecreate = models.DateTimeField(_("Создана"), auto_now_add=True)
    dateclose = models.DateTimeField(
        _("Дата закрытия"), auto_now_add=False, blank=True, null=True
    )
    author = models.ForeignKey(
        "auth.User",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="feedback_ticket_user",
        verbose_name=_("Автор"),
    )
    requeststatuscode = models.IntegerField(
        _("Код завершения операции"), blank=True, null=True
    )
    id_remote = models.IntegerField(
        _("ID тикета в удалённой системе"), null=True, blank=True
    )
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def object_name(self):
        return ("fdb_tckt", _("Тикет"))

    @property
    # суммарная стоимость по Комментам к Тикету
    def costcommentsum(self):
        return FeedbackTicketComment.objects.filter(ticket_id=self.id).aggregate(
            Sum("cost")
        )

    # суммарная стоимость по Задачам (сколько запланировано средств)
    def costtasksum(self):
        return FeedbackTask.objects.filter(ticket_id=self.id).aggregate(Sum("cost"))

    @property
    # суммарная стоимость по Комментариям (сколько освоено средств)
    def costtaskcommentsum(self):
        return FeedbackTaskComment.objects.filter(task__ticket_id=self.id).aggregate(
            Sum("cost")
        )

    @property
    # суммарная затраченное время по Комментариям
    def timesum(self):
        return FeedbackTaskComment.objects.filter(task__ticket_id=self.id).aggregate(
            Sum("time")
        )

    def get_absolute_url(self):
        return reverse(
            "my_feedback:feedbacktasks",
            kwargs={"is_ticketslist_dev": 0, "ticketid": self.pk, "pk": 0},
        )
        # return reverse('my_feedback:feedbacktasks')

    def __str__(self):
        return self.name + " (" + self.datecreate.strftime("%d.%m.%Y, %H:%M") + ")"

    class MPTTMeta:
        order_insertion_by = ["-datecreate"]

    class Meta:
        verbose_name = _("Тикет")
        verbose_name_plural = _("Тикеты")


class FeedbackTask(SetPropertiesDashboardMixin, MPTTModel):
    name = models.CharField(_("Наименование"), max_length=128)
    description = RichTextUploadingField(_("Описание"))
    datebegin = models.DateTimeField(_("Начало"))
    dateend = models.DateTimeField(_("Окончание"))
    ticket = models.ForeignKey(
        "FeedbackTicket",
        on_delete=models.CASCADE,
        related_name="resultticket",
        verbose_name=_("Тикет"),
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
        related_name="ticket_task_assigner",
        verbose_name=_("Исполнитель"),
    )
    cost = models.DecimalField(_("Стоимость"), max_digits=12, decimal_places=2)
    percentage = models.DecimalField(
        _("Процент выполнения"), max_digits=5, decimal_places=2, default=0
    )
    # structure_type = models.ForeignKey('Dict_TaskStructureType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='task_structure_type', verbose_name="Тип задачи в иерархии")
    # type = models.ForeignKey('Dict_TaskType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='project_type', verbose_name="Тип")
    status = models.ForeignKey(
        "Dict_FeedbackTaskStatus",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="feedback_taskstatus",
        verbose_name=_("Статус"),
    )
    datecreate = models.DateTimeField(_("Создана"), auto_now_add=True)
    dateclose = models.DateTimeField(
        _("Дата закрытия"), auto_now_add=False, blank=True, null=True
    )
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="feedback_task_user",
        verbose_name=_("Автор"),
    )
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def object_name(self):
        return ("fdb_tsk", _("Задача тикета"))

    @property
    # суммарная стоимость по Комментариям (сколько освоено средств)
    def costsum(self):
        return FeedbackTaskComment.objects.filter(task_id=self.id).aggregate(
            Sum("cost")
        )

    @property
    # суммарная затраченное время по Комментариям
    def timesum(self):
        return FeedbackTaskComment.objects.filter(task_id=self.id).aggregate(
            Sum("time")
        )

    def get_absolute_url(self):
        return reverse("my_feedback:feedbacktaskcomments", kwargs={"taskid": self.pk})

    def __str__(self):
        return (
            str(self.ticket)
            + ". "
            + self.name
            + " ("
            + self.datebegin.strftime("%d.%m.%Y, %H:%M")
            + " - "
            + self.dateend.strftime("%d.%m.%Y, %H:%M")
            + ")"
        )

    class MPTTMeta:
        order_insertion_by = ["dateend"]

    class Meta:
        verbose_name = _("Задача")
        verbose_name_plural = _("Задачи")


class FeedbackTicketComment(Comment_Model):
    time = models.DecimalField(
        _("Время работы, час."),
        null=True,
        blank=True,
        max_digits=6,
        decimal_places=2,
        default=0,
    )
    cost = models.DecimalField(
        _("Стоимость"), null=True, blank=True, max_digits=9, decimal_places=2, default=0
    )
    ticket = models.ForeignKey(
        "FeedbackTicket",
        on_delete=models.CASCADE,
        related_name="feedback_ticket",
        verbose_name=_("Тикет"),
    )
    company = models.ForeignKey(
        "companies.Company",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="feedback_commentcompany",
        verbose_name=_("Компания"),
    )
    author = models.ForeignKey(
        "auth.User",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("Автор"),
    )
    requeststatuscode = models.IntegerField(
        _("Код завершения операции"), blank=True, null=True
    )
    id_remote = models.IntegerField(
        _("ID комментария в удалённой системе"), null=True, blank=True
    )

    def get_absolute_url(self):
        return reverse(
            "my_feedback:feedbacktasks",
            kwargs={"is_ticketslist_dev": 0, "ticketid": self.ticket_id, "pk": 0},
        )

    def __str__(self):
        return (
            str(self.ticket)
            + ". "
            + self.name
            + " ("
            + self.datecreate.strftime("%d.%m.%Y, %H:%M")
            + ")"
        )

    @property
    def files(self):
        return FeedbackFile.objects.filter(taskcomment_id=self.id, is_active=True)

    class Meta:
        verbose_name = _("Комментарий тикета")
        verbose_name_plural = _("Комментарии тикетов")


class FeedbackTaskComment(Comment_Model):
    task = models.ForeignKey(
        "FeedbackTask",
        on_delete=models.CASCADE,
        related_name="resulttask",
        verbose_name=_("Задача"),
    )

    def get_absolute_url(self):
        return reverse(
            "my_feedback:feedbacktaskcomments", kwargs={"taskid": self.task_id}
        )

    @property
    def files(self):
        return FeedbackFile.objects.filter(taskcomment_id=self.id, is_active=True)

    class Meta:
        verbose_name = _("Комментарий задачи")
        verbose_name_plural = _("Комментарии задач")


class FeedbackFile(models.Model):
    name = models.CharField(_("Наименование"), null=True, blank=True, max_length=255)
    uname = models.CharField(
        _("Уникальное наименование"), null=True, blank=True, max_length=255
    )
    ticket = models.ForeignKey(
        "FeedbackTicket",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="feedbackticket_file",
        verbose_name=_("Тикет"),
    )
    ticketcomment = models.ForeignKey(
        "FeedbackTicketComment",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="ticketcomment_file",
        verbose_name=_("Комментарий тикета"),
    )
    task = models.ForeignKey(
        "FeedbackTask",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="feedbacktask_file",
        verbose_name=_("Задача"),
    )
    taskcomment = models.ForeignKey(
        "FeedbackTaskComment",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="feedbacktaskcomment_file",
        verbose_name=_("Комментарий задачи"),
    )
    pfile = models.FileField(
        upload_to="uploads/files/feedback",
        blank=True,
        null=True,
        verbose_name=_("Файл"),
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
