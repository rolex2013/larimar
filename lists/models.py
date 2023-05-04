from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from main.utils_lang import TranslateFieldMixin

exposed_request = ''

class Dict_YListFieldType(TranslateFieldMixin, models.Model):
    name_ru = models.CharField(_("Наименование_ru"), max_length=128)
    name_en = models.CharField(_("Наименование_en"), max_length=128)
    description_ru = models.TextField(_("Описание_ru"), blank=True, null=True)
    description_en = models.TextField(_("Описание_en"), blank=True, null=True)
    sort = models.PositiveSmallIntegerField(_("Сортировка"), default=1, blank=True, null=True)
    is_active = models.BooleanField(_("Активность"), default=True)
    @property
    def name(self):
        return self.trans_field(exposed_request, 'name')
    @property
    def description(self):
        return self.trans_field(exposed_request, 'description')

    class Meta:
        ordering = ('sort',)
        verbose_name = _('Тип данных')
        verbose_name_plural = _('Типы данных')
    def __str__(self):
        return (self.name)

class YList(models.Model):
    name = models.CharField(_("Наименование"), max_length=128)
    description = models.TextField(_("Описание"), blank=True, null=True)
    fieldslist = models.CharField(_("Список и тип полей"), max_length=1024)
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='ylistresultcompany', verbose_name=_("Компания"))
    datecreate = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    dateupdate = models.DateTimeField(_("Дата изменения"), auto_now_add=True)
    dateclose = models.DateTimeField(_("Дата закрытия"), blank=True, null=True)
    authorupdate = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='ylist_author_update', verbose_name=_("Автор последних "
                                                                                                                            "изменений"))
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='ylist_author', verbose_name=_("Автор"))
    members = models.ManyToManyField('auth.User', related_name='ylist_members', verbose_name=_("Участники"))
    is_active = models.BooleanField(_("Активность Списка"), default=True)

    def get_absolute_url(self):
        return reverse('my_list:ylist_items', kwargs={'pk': self.pk})

    def __str__(self):
        return (self.name + ' ' + self.datecreate.strftime('%d.%m.%Y %H:%M:%S') + ' ' + str(self.author))

class YListItem(models.Model):
    fieldslist = models.TextField(_("Список и значения полей"), blank=True, null=True)
    ylist = models.ForeignKey('YList', on_delete=models.CASCADE, related_name='ylistresult', verbose_name=_("Список"))
    datecreate = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    dateupdate = models.DateTimeField(_("Дата изменения"), auto_now_add=True)
    dateclose = models.DateTimeField(_("Дата закрытия"), auto_now_add=True)
    authorupdate = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='ylistitem_author_update', verbose_name=_("Автор последних "
                                                                                                                            "изменений"))
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='ylistitem_author', verbose_name=_("Автор"))
    is_active = models.BooleanField(_("Активность элемента Списка"), default=True)

    def __str__(self):
        return (self.datecreate.strftime('%d.%m.%Y %H:%M:%S') + '|' + self.name)
