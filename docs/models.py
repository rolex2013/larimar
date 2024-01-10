from django.db import models

from django.urls import reverse  # , reverse_lazy
# from datetime import datetime  # , date, timedelta

from django.utils.translation import gettext_lazy as _

# from mptt.models import MPTTModel, TreeForeignKey

from ckeditor_uploader.fields import RichTextUploadingField

# from main.models import ModelLog
from companies.models import Company

from dashboard.utils import SetPropertiesDashboardMixin


class Dict_DocType(models.Model):
    name = models.CharField("Наименование", max_length=64)
    description = models.TextField("Описание", blank=True, null=True)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)

    class Meta:
        ordering = ("sort",)
        verbose_name = "Тип документ"
        verbose_name_plural = "Типы документов"

    def __str__(self):
        return self.name


class Dict_DocStatus(models.Model):
    name = models.CharField("Наименование", max_length=64)
    description = models.TextField("Описание", blank=True, null=True)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    # is_close = models.BooleanField("Закрывает документ", default=False)
    is_public = models.BooleanField("Публикует версию документа", default=False)
    is_active = models.BooleanField("Активность", default=True)

    class Meta:
        ordering = ("sort",)
        verbose_name = "Статус документа"
        verbose_name_plural = "Статусы документов"

    def __str__(self):
        return self.name


class Dict_DocTaskType(models.Model):
    name = models.CharField("Наименование", max_length=64)
    description = models.TextField("Описание", blank=True, null=True)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)

    class Meta:
        ordering = ("sort",)
        verbose_name = "Тип задачи"
        verbose_name_plural = "Типы задач"

    def __str__(self):
        return self.name


class Dict_DocTaskStatus(models.Model):
    name = models.CharField("Наименование", max_length=64)
    description = models.TextField("Описание", blank=True, null=True)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_close = models.BooleanField("Закрывает задачу", default=False)
    is_active = models.BooleanField("Активность", default=True)

    class Meta:
        ordering = ("sort",)
        verbose_name = "Статус задачи"
        verbose_name_plural = "Статусы задач"

    def __str__(self):
        return self.name


class Doc(models.Model):
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="result_company_doc",
        verbose_name="Организация",
    )
    manager = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="result_manager_doc",
        verbose_name="Менеджер документа",
    )
    name = models.CharField("Наименование", max_length=64)
    type = models.ForeignKey(
        "Dict_DocType",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="doc_type_doc",
        verbose_name="Тип документа",
    )
    status = models.ForeignKey(
        "Dict_DocStatus",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="doc_status_doc",
        verbose_name="Статус документа",
    )
    description = RichTextUploadingField("Описание", blank=True, null=True)
    datecreate = models.DateTimeField("Создан", auto_now_add=True)
    datepublic = models.DateTimeField(
        "Дата публикации", auto_now_add=False, blank=True, null=True
    )
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="doc_author",
        verbose_name="Автор",
    )
    members = models.ManyToManyField(
        "auth.User", related_name="doc_members", verbose_name="Участники"
    )
    is_active = models.BooleanField("Активность", default=True)

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
        # cnt = DocTask.objects.filter(doc_id=self.id, docver_id=self.docver, is_active=True).exclude(dateclose=None).count()
        # print('cnt='+str(cnt))
        # return DocTask.objects.filter(doc_id=self.id, docver_id=self.docver, is_active=True).exclude(dateclose=None).count() #cnt
        # return DocTask.objects.filter(doc_id=self.id, is_active=True).exclude(dateclose=None).count()  # cnt
        return DocTask.objects.filter(
            doc_id=self.id, is_active=True, dateclose=None
        ).count()

    def get_absolute_url(self):
        # return reverse('my_doc:doctasks', kwargs={'docverid': self.docver, 'pk': self.pk})
        return reverse("my_doc:doctasks", kwargs={"pk": self.pk})
        # return reverse('my_crm:clients0')

    def __str__(self):
        return (
            self.name
            + " ("
            + self.datecreate.strftime("%d.%m.%Y, %H:%M")
            + " "
            + self.author.username
            + ") вер. "
            + str(self.docver)
        )

    class Meta:
        # unique_together = ('user','company')
        # ordering = ('user')
        verbose_name = "Документ"
        verbose_name_plural = "Документы"


class DocVer(models.Model):
    # company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='docver_company', verbose_name="Организация")
    vernumber = models.PositiveIntegerField("Номер версии")
    doc = models.ForeignKey(
        "Doc",
        on_delete=models.CASCADE,
        related_name="docver_doc",
        verbose_name="Документ",
    )
    manager = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="docver_manager",
        verbose_name="Менеджер документа",
    )
    name = models.CharField("Наименование", max_length=64)
    type = models.ForeignKey(
        "Dict_DocType",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="docver_type",
        verbose_name="Тип документа",
    )
    status = models.ForeignKey(
        "Dict_DocStatus",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="docver_status",
        verbose_name="Статус документа",
    )
    description = RichTextUploadingField("Описание", blank=True, null=True)
    datecreate = models.DateTimeField("Создан", auto_now_add=True)
    datepublic = models.DateTimeField(
        "Дата публикации", auto_now_add=False, blank=True, null=True
    )
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="docver_author",
        verbose_name="Автор",
    )
    members = models.ManyToManyField(
        "auth.User", related_name="docver_members", verbose_name="Участники"
    )
    is_public = models.BooleanField("Опубликована", default=False)
    is_actual = models.BooleanField("Актуальность", default=False)
    is_active = models.BooleanField("Активность", default=True)

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
        verbose_name = "Версия Документа"
        verbose_name_plural = "Версии Документов"


class DocTask(SetPropertiesDashboardMixin, models.Model):
    name = models.CharField("Наименование", max_length=128)
    description = RichTextUploadingField("Описание", null=True, blank=True)
    # datebegin = models.DateTimeField("Начало")
    dateend = models.DateField("Окончание")
    doc = models.ForeignKey(
        "Doc",
        on_delete=models.CASCADE,
        related_name="resultdoc",
        verbose_name="Документ",
    )
    docver = models.ForeignKey(
        "DocVer",
        on_delete=models.CASCADE,
        related_name="resultdocver",
        verbose_name="Версия Документа",
    )
    assigner = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="doctask_assigner",
        verbose_name="Исполнитель",
    )
    type = models.ForeignKey(
        "Dict_DocTaskType",
        null=True,
        blank=True,
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="doctask_type",
        verbose_name="Тип",
    )
    status = models.ForeignKey(
        "Dict_DocTaskStatus",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="doctask_status",
        verbose_name="Статус",
    )
    datecreate = models.DateTimeField("Дата создания", auto_now_add=True)
    dateclose = models.DateTimeField(
        "Дата закрытия", auto_now_add=False, blank=True, null=True
    )
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="resultdoctaskuser",
        verbose_name="Автор",
    )
    is_active = models.BooleanField("Активность", default=True)

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
            + " (Срок: "
            + self.dateend.strftime("%d.%m.%Y")
            + ")"
        )

    class MPTTMeta:
        # order_insertion_by = ['name']
        order_insertion_by = ["-dateend"]

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"


class DocTaskComment(models.Model):
    # name = models.CharField("Наименование", max_length=128)
    description = RichTextUploadingField("Текст")
    time = models.DecimalField(
        "Время работы, час.",
        max_digits=6,
        decimal_places=2,
        blank=False,
        null=False,
        default=0,
    )
    cost = models.DecimalField("Стоимость", max_digits=9, decimal_places=2, default=0)
    task = models.ForeignKey(
        "DocTask",
        on_delete=models.CASCADE,
        related_name="resultdoctask",
        verbose_name="Задача",
    )
    datecreate = models.DateTimeField("Создан", auto_now_add=True)
    author = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, verbose_name="Автор"
    )
    is_active = models.BooleanField("Активность", default=True)

    def get_absolute_url(self):
        return reverse("my_doc:doctaskcomments", kwargs={"taskid": self.task_id})

    def __str__(self):
        # return (str(self.task) + '. ' + self.name + ' (' + self.datecreate.strftime('%d.%m.%Y, %H:%M') + ')')
        return (
            str(self.task)
            + ". "
            + " ("
            + self.author
            + " | "
            + self.datecreate.strftime("%d.%m.%Y, %H:%M")
            + ")"
        )

    @property
    def files(self):
        return DocVerFile.objects.filter(taskcomment_id=self.id, is_active=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class DocVerFile(models.Model):
    name = models.CharField("Наименование", null=True, blank=True, max_length=255)
    uname = models.CharField(
        "Уникальное наименование", null=True, blank=True, max_length=255
    )
    doc = models.ForeignKey(
        "Doc",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="doc_file",
        verbose_name="Документ",
    )
    docver = models.ForeignKey(
        "DocVer",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="docver_file",
        verbose_name="Версия Документа",
    )
    task = models.ForeignKey(
        "DocTask",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="doctask_file",
        verbose_name="Задача",
    )
    taskcomment = models.ForeignKey(
        "DocTaskComment",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="doctaskcomment_file",
        verbose_name="Комментарий",
    )
    pfile = models.FileField(
        upload_to="uploads/files/docs", blank=True, null=True, verbose_name="Файл"
    )
    psize = models.PositiveIntegerField(editable=False, null=True, blank=True)
    datecreate = models.DateTimeField("Создан", auto_now_add=True)
    author = models.ForeignKey(
        "auth.User",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    is_active = models.BooleanField("Активность", default=True)

    class Meta:
        verbose_name = "Файлы"
        verbose_name_plural = "Файлы"

    def __str__(self):
        return str(self.id) + " " + self.uname
