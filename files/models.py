from django.db import models
from django.db.models import Q, Sum

from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey
from main.models import ModelLog, Dict_Theme

# from ckeditor_uploader.fields import RichTextUploadingField
from django_ckeditor_5.fields import CKEditor5Field

# from companies.models import Company

# from main.utils_lang import TranslateFieldMixin
from main.utils_model import Dict_Model


exposed_request = ""


class Dict_FolderType(Dict_Model):
    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    class Meta:
        verbose_name = _("Тип содержимого папки")
        verbose_name_plural = _("Типы содержимого папок")


class Folder(MPTTModel):
    name = models.CharField(_("Наименование"), max_length=64)
    description = models.TextField(_("Описание"), blank=True, null=True)
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="result_company_folder",
        verbose_name=_("Компания"),
    )
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="folder_children",
        verbose_name=_("Папка верхнего уровня"),
    )
    theme = models.ForeignKey(
        "main.Dict_Theme",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="folder_theme",
        verbose_name=_("Тематика"),
    )
    type = models.ForeignKey(
        "Dict_FolderType",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="folder_type",
        verbose_name=_("Тип"),
    )
    # status = models.ForeignKey('Dict_FolderStatus', limit_choices_to={'is_active': True}, on_delete=models.CASCADE,
    #                           related_name='folder_status', verbose_name="Статус")
    datecreate = models.DateTimeField(_("Создан"), auto_now_add=True)
    # dateclose = models.DateTimeField("Дата закрытия", auto_now_add=False, blank=True, null=True)
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="folder_author",
        verbose_name=_("Автор"),
    )
    # members = models.ManyToManyField('auth.User', related_name='project_members', verbose_name="Участники")
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    # всего файлов в Папке
    def filecount(self):
        return FolderFile.objects.filter(folder_id=self.id, is_active=True).count()

    def get_absolute_url(self):
        # return reverse('my_file:files', kwargs={'folderid': self.pk, 'pk': '0'})
        return reverse(
            "my_file:folders", kwargs={"companyid": self.company_id, "pk": self.pk}
        )

    def __str__(self):
        # return (self.name + ' (' + self.datebegin.strftime('%d.%m.%Y') + '-' + self.dateend.strftime(
        #   '%d.%m.%Y') + ' / ' + self.datecreate.strftime('%d.%m.%Y %H:%M:%S') + ')')
        return self.name

    class Meta:
        verbose_name = _("Папка")
        verbose_name_plural = _("Папки")


class FolderFile(models.Model):
    name = models.CharField(_("Наименование"), null=True, blank=True, max_length=255)
    uname = models.CharField(
        _("Уникальное наименование"), null=True, blank=True, max_length=255
    )
    folder = models.ForeignKey(
        "Folder",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="folder_file",
        verbose_name=_("Папка"),
    )
    pfile = models.FileField(
        upload_to="uploads/files/files", blank=True, null=True, verbose_name=_("Файл")
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
        return str(self.id) + " " + self.uname
