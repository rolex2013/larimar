from django.db import models
from django.db.models import Sum

from django.urls import reverse  # , reverse_lazy

# from datetime import datetime

from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

# from main.models import ModelLog

from ckeditor_uploader.fields import RichTextUploadingField

# from companies.models import Company

from dashboard.utils import SetPropertiesDashboardMixin
from main.utils_model import Dict_Model


exposed_request = ""


# import json
# from datetime import datetime, timedelta
# import pytz


# class Dict_ProjectStatus(models.Model):
#     name = models.CharField("Наименование", max_length=64)
#     sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
#     name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
#     is_close = models.BooleanField("Закрывает проект", default=False)
#     is_active = models.BooleanField("Активность", default=True)
#     class Meta:
#         ordering = ('sort',)
#         verbose_name = 'Статус проекта'
#         verbose_name_plural = 'Статусы проектов'
#     def __str__(self):
#         return (self.name)


class Dict_ProjectStatus(Dict_Model):
    is_close = models.BooleanField(_("Закрывает проект"), default=False)

    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    class Meta:
        verbose_name = _("Статус проекта")
        verbose_name_plural = _("Статусы проектов")


class Dict_ProjectStructureType(Dict_Model):
    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    class Meta:
        verbose_name = _("Тип проектов в иерархии")
        verbose_name_plural = _("Типы проектов в иерархии")


class Dict_ProjectType(Dict_Model):
    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    class Meta:
        verbose_name = _("Тип проекта")
        verbose_name_plural = _("Типы проектов")


class Dict_TaskStatus(Dict_Model):
    is_close = models.BooleanField(_("Закрывает задачу"), default=False)

    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    class Meta:
        verbose_name = _("Статус задачи")
        verbose_name_plural = _("Статусы задач")


class Dict_TaskStructureType(Dict_Model):
    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    class Meta:
        verbose_name = _("Тип задачи в иерархии")
        verbose_name_plural = _("Типы задач в иерархии")


class Dict_TaskType(Dict_Model):
    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    class Meta:
        verbose_name = _("Тип задачи")
        verbose_name_plural = _("Типы задач")


class Project(SetPropertiesDashboardMixin, MPTTModel):
    name = models.CharField(_("Наименование"), max_length=64)
    description = RichTextUploadingField(_("Описание"))
    datebegin = models.DateField(_("Начало"))
    dateend = models.DateField(_("Окончание"))
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="resultcompany",
        verbose_name=_("Компания"),
    )
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="project_children",
        verbose_name=_("Проект верхнего уровня"),
    )
    assigner = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="project_assigner",
        verbose_name=_("Исполнитель"),
    )
    currency = models.ForeignKey(
        "finance.Dict_Currency",
        on_delete=models.CASCADE,
        related_name="resultcurrency",
        verbose_name=_("Валюта"),
    )
    cost = models.DecimalField(
        _("Стоимость"), max_digits=12, decimal_places=2, default=0
    )
    percentage = models.DecimalField(
        _("Процент выполнения"), max_digits=5, decimal_places=2, default=0
    )
    structure_type = models.ForeignKey(
        "Dict_ProjectStructureType",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="project_structure_type",
        verbose_name=_("Тип в иерархии"),
    )
    type = models.ForeignKey(
        "Dict_ProjectType",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="project_type",
        verbose_name=_("Тип"),
    )
    status = models.ForeignKey(
        "Dict_ProjectStatus",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="project_status",
        verbose_name=_("Статус"),
    )
    datecreate = models.DateTimeField(_("Создан"), auto_now_add=True)
    dateclose = models.DateTimeField(
        _("Дата закрытия"), auto_now_add=False, blank=True, null=True
    )
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="project_author",
        verbose_name=_("Автор"),
    )
    members = models.ManyToManyField(
        "auth.User", related_name="project_members", verbose_name=_("Участники")
    )
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def object_name(self):
        return ("prj_prj", _("Проект"))

    @property
    def link(self):
        index = str(self.pk)
        # print(index[-1].__class__.__name__)
        return f"my_project:tasks {index} 0"  # + str(self.pk)
        # return mark_safe(f"{ my_project:tasks {index} 0 %}")

    @property
    # суммарная стоимость по Комментам (сколько освоено средств)
    def costsum(self):
        return TaskComment.objects.filter(task__project_id=self.id).aggregate(
            Sum("cost")
        )

    @property
    # суммарная затраченное время по Комментам
    def timesum(self):
        return TaskComment.objects.filter(task__project_id=self.id).aggregate(
            Sum("time")
        )

    def get_absolute_url(self):
        return reverse("my_project:tasks", kwargs={"projectid": self.pk, "pk": "0"})

    def __str__(self):
        return (
            self.name
            + " ("
            + self.datebegin.strftime("%d.%m.%Y")
            + "-"
            + self.dateend.strftime("%d.%m.%Y")
            + " / "
            + self.datecreate.strftime("%d.%m.%Y %H:%M:%S")
            + ")"
        )

    """
    def save(self, *args, **kwargs):
        # Получаем старые значения для дальнейшей проверки на изменения
        old = Project.objects.filter(pk=self.pk).first() # вместо objects.get(), чтоб не вызывало исключения при создании нового проекта
        super().save(*args, **kwargs)
        if old:
           historyjson = {"Проект":'' if self.name == old.name else self.name,
                          "Статус":'' if self.status.name == old.status.name else self.status.name, 
                          "Начало":'' if self.datebegin == old.datebegin else self.datebegin.strftime('%d.%m.%Y'), 
                          "Окончание":'' if self.dateend == old.dateend else self.dateend.strftime('%d.%m.%Y'),
                          "Тип в иерархии":'' if self.structure_type.name == old.structure_type.name else self.structure_type.name,
                          "Тип":'' if self.type.name == old.type.name else self.type.name,
                          "Стоимость":'' if self.cost == old.cost else str(self.cost),
                          "Валюта":'' if self.currency.code_char == old.currency.code_char else str(self.currency.code_char),
                          "Выполнен на, %":'' if self.percentage == old.percentage else str(self.percentage),
                          "Исполнитель":'' if self.assigner.username == old.assigner.username else self.assigner.username,
                          "Активность":'' if self.is_active == old.is_active else '✓' if self.is_active else '-'
                          #, "Участники":self.members.username
                         }                                     
        else:
           historyjson = {"Проект": self.name,
                          "Статус": self.status.name, 
                          "Начало": self.datebegin.strftime('%d.%m.%Y'), 
                          "Окончание": self.dateend.strftime('%d.%m.%Y'),
                          "Тип в иерархии": self.structure_type.name,
                          "Тип": self.type.name,
                          "Стоимость": str(self.cost),
                          "Валюта": str(self.currency.code_char),
                          "Выполнен на, %": str(self.percentage),
                          "Исполнитель": self.assigner.username,
                          "Активность": '✓' if self.is_active else '-'
                          #, "Участники":self.members.username
                         }                                     
        ModelLog.objects.create(componentname='prj', modelname="Project", modelobjectid=self.id, author=self.author, log=json.dumps(historyjson))
    """

    class Meta:
        verbose_name = _("Проект")
        verbose_name_plural = _("Проекты")


class Task(SetPropertiesDashboardMixin, MPTTModel):
    name = models.CharField(_("Наименование"), max_length=128)
    description = RichTextUploadingField(_("Описание"))
    datebegin = models.DateTimeField(_("Начало"))
    dateend = models.DateTimeField(_("Окончание"))
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        related_name="resultproject",
        verbose_name=_("Проект"),
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
        related_name="task_assigner",
        verbose_name=_("Исполнитель"),
    )
    cost = models.DecimalField(_("Стоимость"), max_digits=12, decimal_places=2)
    percentage = models.DecimalField(
        _("Процент выполнения"), max_digits=5, decimal_places=2, default=0
    )
    structure_type = models.ForeignKey(
        "Dict_TaskStructureType",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="task_structure_type",
        verbose_name=_("Тип задачи в иерархии"),
    )
    type = models.ForeignKey(
        "Dict_TaskType",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="project_type",
        verbose_name=_("Тип"),
    )
    status = models.ForeignKey(
        "Dict_TaskStatus",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="project_status",
        verbose_name=_("Статус"),
    )
    datecreate = models.DateTimeField(_("Создана"), auto_now_add=True)
    dateclose = models.DateTimeField(
        _("Дата закрытия"), auto_now_add=False, blank=True, null=True
    )
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="resultuser",
        verbose_name=_("Автор"),
    )
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    # суммарная стоимость по Комментариям (сколько освоено средств)
    def costsum(self):
        return TaskComment.objects.filter(task_id=self.id).aggregate(Sum("cost"))

    @property
    # суммарная затраченное время по Комментариям
    def timesum(self):
        return TaskComment.objects.filter(task_id=self.id).aggregate(Sum("time"))

    @property
    def object_name(self):
        return ("prj_tsk", _("Задача проекта"))

    @property
    def link(self):
        index = str(self.pk)
        return f"my_project:taskcomments {index}"  # + str(self.pk)

    def get_absolute_url(self):
        return reverse("my_project:taskcomments", kwargs={"taskid": self.pk})
        # return reverse('my_project:taskcomments, kwargs={'taskid': self.pk})

    def __str__(self):
        return (
            str(self.project)
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
        order_insertion_by = ["dateend"]

    class Meta:
        verbose_name = _("Задача")
        verbose_name_plural = _("Задачи")


class TaskComment(models.Model):
    name = models.CharField(_("Наименование"), max_length=128)
    description = RichTextUploadingField(_("Описание"))
    time = models.DecimalField(
        _("Время работы, час."),
        max_digits=6,
        decimal_places=2,
        blank=False,
        null=False,
        default=0,
    )
    cost = models.DecimalField(
        _("Стоимость"), max_digits=9, decimal_places=2, default=0
    )
    task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        related_name="resulttask",
        verbose_name=_("Задача"),
    )
    datecreate = models.DateTimeField(_("Создан"), auto_now_add=True)
    author = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, verbose_name=_("Автор")
    )
    is_active = models.BooleanField(_("Активность"), default=True)

    def get_absolute_url(self):
        return reverse("my_project:taskcomments", kwargs={"taskid": self.task_id})

    def __str__(self):
        return (
            str(self.task)
            + ". "
            + self.name
            + " ("
            + self.datecreate.strftime("%d.%m.%Y, %H:%M")
            + ")"
        )

    @property
    def files(self):
        return ProjectFile.objects.filter(taskcomment_id=self.id, is_active=True)

    class Meta:
        verbose_name = _("Комментарий")
        verbose_name_plural = _("Комментарии")


class ProjectFile(models.Model):
    name = models.CharField(_("Наименование"), null=True, blank=True, max_length=255)
    uname = models.CharField(
        _("Уникальное наименование"), null=True, blank=True, max_length=255
    )
    project = models.ForeignKey(
        "Project",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="project_file",
        verbose_name=_("Проект"),
    )
    task = models.ForeignKey(
        "Task",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="task_file",
        verbose_name=_("Задача"),
    )
    taskcomment = models.ForeignKey(
        "TaskComment",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="taskcomment_file",
        verbose_name=_("Комментарий"),
    )
    pfile = models.FileField(
        upload_to="uploads/files/projects",
        blank=True,
        null=True,
        verbose_name=_("Файл"),
    )
    # psize = models.CharField(editable=False, max_length=64)
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
