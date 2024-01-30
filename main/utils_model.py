from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel
from ckeditor_uploader.fields import RichTextUploadingField

# exposed_request = ''


class TranslateFieldMixin(object):
    model = None
    model_form = None
    template = None

    def trans_field(self, exposed_request, name):
        try:
            # lang = exposed_request.session[settings.LANGUAGE_SESSION_KEY]
            lang = exposed_request.COOKIES[settings.LANGUAGE_COOKIE_NAME]
        except KeyError:
            try:
                lang = exposed_request.session[settings.LANGUAGE_COOKIE_NAME]
            except KeyError:
                lang = "ru"

        if lang is None:
            lang = "ru"

        return getattr(self, name + "_" + lang, None)


class Dict_Model(TranslateFieldMixin, models.Model):
    name_ru = models.CharField(_("Наименование_ru"), max_length=64)
    name_en = models.CharField(
        _("Наименование_en"), max_length=64, blank=True, null=True
    )
    description_ru = models.TextField(_("Описание_ru"), blank=True, null=True)
    description_en = models.TextField(_("Описание_en"), blank=True, null=True)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    is_active = models.BooleanField(_("Активность"), default=True)

    # @property
    # def name(self):
    #     return self.trans_field(models.exposed_request, "name")

    def __str__(self):
        return self.name if self.name else self.name_ru

    # def trans_field(self, exp_req, name):
    #     try:
    #         lang = exp_req.COOKIES[settings.LANGUAGE_COOKIE_NAME]
    #     except KeyError:
    #         try:
    #             lang = exp_req.session[settings.LANGUAGE_COOKIE_NAME]
    #         except KeyError:
    #             lang = "ru"
    #     if lang is None:
    #         lang = "ru"

    #     return getattr(self, name + "_" + lang, None)

    class Meta:
        abstract = True
        ordering = ("sort",)


class Task_Model(MPTTModel):
    name = models.CharField(_("Наименование"), max_length=128)
    description = RichTextUploadingField(_("Описание"), null=True, blank=True)
    datebegin = models.DateTimeField(_("Начало"))
    dateend = models.DateTimeField(_("Окончание"))
    percentage = models.DecimalField(
        _("Процент выполнения"), max_digits=5, decimal_places=2, default=0
    )
    datecreate = models.DateTimeField(_("Создана"), auto_now_add=True)
    dateclose = models.DateTimeField(
        _("Дата закрытия"), auto_now_add=False, blank=True, null=True
    )
    is_active = models.BooleanField(_("Активность"), default=True)

    class MPTTMeta:
        order_insertion_by = ["dateend"]

    class Meta:
        abstract = True
        verbose_name = _("Задача")
        verbose_name_plural = _("Задачи")


class Comment_Model(models.Model):
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
    datecreate = models.DateTimeField(_("Создан"), auto_now_add=True)
    author = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, verbose_name=_("Автор")
    )
    is_active = models.BooleanField(_("Активность"), default=True)

    def __str__(self):
        return (
            str(self.task)
            + ". "
            + self.name
            + " ("
            + self.datecreate.strftime("%d.%m.%Y, %H:%M")
            + ")"
        )

    class Meta:
        abstract = True
