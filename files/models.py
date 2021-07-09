from django.db import models
from django.db.models import Q, Sum

from django.urls import reverse, reverse_lazy
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey
from main.models import ModelLog, Dict_Theme

from ckeditor_uploader.fields import RichTextUploadingField

from companies.models import Company


class Dict_FolderType(models.Model):
    name = models.CharField("Наименование", max_length=64)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Тип содержимого папки'
        verbose_name_plural = 'Типы содержимого папок'
    def __str__(self):
        return (self.name)

class Folder(MPTTModel):
    name = models.CharField("Наименование", max_length=64)
    description = RichTextUploadingField("Описание", blank=True, null=True)
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='result_company_folder',
                                verbose_name="Компания")
    parent = TreeForeignKey('self', null=True, blank=True, limit_choices_to={'is_active': True},
                            on_delete=models.CASCADE, related_name='folder_children',
                            verbose_name="Папка верхнего уровня")
    theme = models.ForeignKey('main.Dict_Theme', limit_choices_to={'is_active': True}, on_delete=models.CASCADE,
                             related_name='folder_theme', verbose_name="Тематика")
    type = models.ForeignKey('Dict_FolderType', limit_choices_to={'is_active': True}, on_delete=models.CASCADE,
                             related_name='folder_type', verbose_name="Тип")
    #status = models.ForeignKey('Dict_FolderStatus', limit_choices_to={'is_active': True}, on_delete=models.CASCADE,
    #                           related_name='folder_status', verbose_name="Статус")
    datecreate = models.DateTimeField("Создан", auto_now_add=True)
    #dateclose = models.DateTimeField("Дата закрытия", auto_now_add=False, blank=True, null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='folder_author',
                               verbose_name="Автор")
    #members = models.ManyToManyField('auth.User', related_name='project_members', verbose_name="Участники")
    is_active = models.BooleanField("Активность", default=True)

    @property
    # всего файлов в Папке
    def filecount(self):
        return FolderFile.objects.filter(folder_id=self.id, is_active=True).count()

    def get_absolute_url(self):
        #return reverse('my_file:files', kwargs={'folderid': self.pk, 'pk': '0'})
        return reverse('my_file:folders', kwargs={'companyid': self.company_id, 'pk': self.pk})

    def __str__(self):
        #return (self.name + ' (' + self.datebegin.strftime('%d.%m.%Y') + '-' + self.dateend.strftime(
        #   '%d.%m.%Y') + ' / ' + self.datecreate.strftime('%d.%m.%Y %H:%M:%S') + ')')
        return (self.name)

    class Meta:
        verbose_name = 'Папка'
        verbose_name_plural = 'Папки'


class FolderFile(models.Model):
    name = models.CharField("Наименование", null=True, blank=True, max_length=255)
    uname = models.CharField("Уникальное наименование", null=True, blank=True, max_length=255)
    folder = models.ForeignKey('Folder', null=True, blank=True, on_delete=models.CASCADE, related_name='folder_file', verbose_name="Папка")
    pfile = models.FileField(upload_to='uploads/files/files', blank=True, null=True, verbose_name='Файл')
    psize = models.CharField(editable=False, max_length=64)
    datecreate = models.DateTimeField("Создан", auto_now_add=True)
    author = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True)

    class Meta:
        verbose_name = "Файлы"
        verbose_name_plural = "Файлы"

    def __str__(self):
        return str(self.id) + ' ' + self.uname