from django.db import models

from django.urls import reverse  # , reverse_lazy

# from datetime import datetime  # , date, timedelta

from django.utils.translation import gettext_lazy as _

# from mptt.models import MPTTModel, TreeForeignKey

from ckeditor_uploader.fields import RichTextUploadingField

# from main.models import ModelLog
from companies.models import Company

from dashboard.utils import SetPropertiesDashboardMixin

from main.utils_lang import TranslateFieldMixin
from main.utils_model import Dict_Model, Comment_Model


exposed_request = ""


class Dict_DocType(TranslateFieldMixin, models.Model):
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
        verbose_name = _("Тип документ")
        verbose_name_plural = _("Типы документов")

    def __str__(self):
        return self.name


class Dict_DocStatus(TranslateFieldMixin, models.Model):
    name_ru = models.CharField(_("Наименование_ru"), max_length=64)
    name_en = models.CharField(_("Наименование_en"), max_length=64)
    description_ru = models.TextField(_("Описание_ru"), blank=True, null=True)
    description_en = models.TextField(_("Описание_en"), blank=True, null=True)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    # is_close = models.BooleanField("Закрывает документ", default=False)
    is_public = models.BooleanField(_("Публикует версию документа"), default=False)
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    class Meta:
        ordering = ("sort",)
        verbose_name = _("Статус документа")
        verbose_name_plural = _("Статусы документов")

    def __str__(self):
        return self.name


class Dict_DocTaskType(TranslateFieldMixin, models.Model):
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
        verbose_name = _("Тип задачи")
        verbose_name_plural = _("Типы задач")

    def __str__(self):
        return self.name


class Dict_DocTaskStatus(TranslateFieldMixin, models.Model):
    name_ru = models.CharField(_("Наименование_ru"), max_length=64)
    name_en = models.CharField(_("Наименование_en"), max_length=64)
    description_ru = models.TextField(_("Описание_ru"), blank=True, null=True)
    description_en = models.TextField(_("Описание_en"), blank=True, null=True)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    is_close = models.BooleanField(_("Закрывает задачу"), default=False)
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    class Meta:
        ordering = ("sort",)
        verbose_name = _("Статус задачи")
        verbose_name_plural = _("Статусы задач")

    def __str__(self):
        return self.name


class Doc(models.Model):
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="result_company_doc",
        verbose_name=_("Организация"),
    )
    manager = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="result_manager_doc",
        verbose_name=_("Менеджер документа"),
    )
    name = models.CharField(_("Наименование"), max_length=64)
    type = models.ForeignKey(
        "Dict_DocType",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="doc_type_doc",
        verbose_name=_("Тип документа"),
    )
    status = models.ForeignKey(
        "Dict_DocStatus",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="doc_status_doc",
        verbose_name=_("Статус документа"),
    )
    description = RichTextUploadingField(_("Описание"), blank=True, null=True)
    datecreate = models.DateTimeField(_("Создан"), auto_now_add=True)
    datepublic = models.DateTimeField(
        _("Дата публикации"), auto_now_add=False, blank=True, null=True
    )
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="doc_author",
        verbose_name=_("Автор"),
    )
    members = models.ManyToManyField(
        "auth.User", related_name="doc_members", verbose_name=_("Участники")
    )
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    # ссылка на текущую версию Документа
    def docver(self):
        return (
            DocVer.objects.filter(doc_id=self.id, is_active=True, is_actual=True)
            .values_list("id", flat=True)
            .first()
        )

    @property
    # кол-во незавершённых задач Документа
    def doctask(self):
        return DocTask.objects.filter(
            doc_id=self.id, is_active=True, dateclose=None
        ).count()

    def get_absolute_url(self):
        return reverse("my_doc:doctasks", kwargs={"pk": self.pk})

    def __str__(self):
        return (
            self.name
            + " ("
            + self.datecreate.strftime("%d.%m.%Y, %H:%M")
            + " "
            + self.author.username
            + ") "
            + _("вер.")
            + " "
            + str(self.docver)
        )

    class Meta:
        # unique_together = ('user','company')
        # ordering = ('user')
        verbose_name = _("Документ")
        verbose_name_plural = _("Документы")


class DocVer(models.Model):
    vernumber = models.PositiveIntegerField(_("Номер версии"))
    doc = models.ForeignKey(
        "Doc",
        on_delete=models.CASCADE,
        related_name="docver_doc",
        verbose_name=_("Документ"),
    )
    manager = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="docver_manager",
        verbose_name=_("Менеджер документа"),
    )
    name = models.CharField(_("Наименование"), max_length=64)
    type = models.ForeignKey(
        "Dict_DocType",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="docver_type",
        verbose_name=_("Тип документа"),
    )
    status = models.ForeignKey(
        "Dict_DocStatus",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="docver_status",
        verbose_name=_("Статус документа"),
    )
    description = RichTextUploadingField(_("Описание"), blank=True, null=True)
    datecreate = models.DateTimeField(_("Создан"), auto_now_add=True)
    datepublic = models.DateTimeField(
        _("Дата публикации"), auto_now_add=False, blank=True, null=True
    )
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="docver_author",
        verbose_name=_("Автор"),
    )
    members = models.ManyToManyField(
        "auth.User", related_name="docver_members", verbose_name=_("Участники")
    )
    is_public = models.BooleanField(_("Опубликована"), default=False)
    is_actual = models.BooleanField(_("Актуальность"), default=False)
    is_active = models.BooleanField(_("Активность"), default=True)

    # def get_absolute_url(self):
    #     return reverse('my_doc:docdetail', kwargs={'docid': self.pk, 'pk': '0'})
    #    #return reverse('my_crm:clients0')
    def __str__(self):
        return (
            self.name
            + " ("
            + self.datecreate.strftime("%d.%m.%Y, %H:%M")
            + " "
            + self.author.username
            + ")"
        )

    class Meta:
        # unique_together = ('company', 'is_actual')
        # ordering = ('user')
        verbose_name = _("Версия Документа")
        verbose_name_plural = _("Версии Документов")


class DocTask(SetPropertiesDashboardMixin, models.Model):
    name = models.CharField(_("Наименование"), max_length=128)
    description = RichTextUploadingField(_("Описание"), null=True, blank=True)
    # datebegin = models.DateTimeField("Начало")
    dateend = models.DateField(_("Окончание"))
    doc = models.ForeignKey(
        "Doc",
        on_delete=models.CASCADE,
        related_name="resultdoc",
        verbose_name=_("Документ"),
    )
    docver = models.ForeignKey(
        "DocVer",
        on_delete=models.CASCADE,
        related_name="resultdocver",
        verbose_name=_("Версия Документа"),
    )
    assigner = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="doctask_assigner",
        verbose_name=_("Исполнитель"),
    )
    type = models.ForeignKey(
        "Dict_DocTaskType",
        null=True,
        blank=True,
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="doctask_type",
        verbose_name=_("Тип"),
    )
    status = models.ForeignKey(
        "Dict_DocTaskStatus",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="doctask_status",
        verbose_name=_("Статус"),
    )
    datecreate = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    dateclose = models.DateTimeField(
        _("Дата закрытия"), auto_now_add=False, blank=True, null=True
    )
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="resultdoctaskuser",
        verbose_name=_("Автор"),
    )
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def object_name(self):
        return ("doc_tsk", _("Задача документа"))

    @property
    def get_absolute_url(self):
        return reverse("my_doc:doctaskcomments", kwargs={"taskid": self.pk})

    def __str__(self):
        return (
            str(self.docver)
            + ". "
            + self.name
            + " ("
            + _("Срок")
            + ": "
            + self.dateend.strftime("%d.%m.%Y")
            + ")"
        )

    class MPTTMeta:
        # order_insertion_by = ['name']
        order_insertion_by = ["-dateend"]

    class Meta:
        verbose_name = _("Задача")
        verbose_name_plural = _("Задачи")


class DocTaskComment(Comment_Model):
    time = models.DecimalField(
        _("Время работы, час."),
        max_digits=6,
        decimal_places=2,
        blank=False,
        null=False,
        default=0,
    )
    task = models.ForeignKey(
        "DocTask",
        on_delete=models.CASCADE,
        related_name="resultdoctask",
        verbose_name=_("Задача"),
    )

    def get_absolute_url(self):
        return reverse("my_doc:doctaskcomments", kwargs={"taskid": self.task_id})

    @property
    def files(self):
        return DocVerFile.objects.filter(taskcomment_id=self.id, is_active=True)

    class Meta:
        verbose_name = _("Комментарий")
        verbose_name_plural = _("Комментарии")


class DocVerFile(models.Model):
    name = models.CharField(_("Наименование"), null=True, blank=True, max_length=255)
    uname = models.CharField(
        _("Уникальное наименование"), null=True, blank=True, max_length=255
    )
    doc = models.ForeignKey(
        "Doc",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="doc_file",
        verbose_name=_("Документ"),
    )
    docver = models.ForeignKey(
        "DocVer",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="docver_file",
        verbose_name=_("Версия Документа"),
    )
    task = models.ForeignKey(
        "DocTask",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="doctask_file",
        verbose_name=_("Задача"),
    )
    taskcomment = models.ForeignKey(
        "DocTaskComment",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="doctaskcomment_file",
        verbose_name=_("Комментарий"),
    )
    pfile = models.FileField(
        upload_to="uploads/files/docs", blank=True, null=True, verbose_name=_("Файл")
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
        return str(self.id) + " " + self.uname
