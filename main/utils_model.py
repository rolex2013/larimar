from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# from main.utils_lang import TranslateFieldMixin


# class Dict_Model(TranslateFieldMixin, models.Model):
class Dict_Model(models.Model):
    name_ru = models.CharField(_("Наименование_ru"), max_length=64)
    name_en = models.CharField(
        _("Наименование_en"), max_length=64, blank=True, null=True
    )
    description_ru = models.TextField(_("Описание_ru"), blank=True, null=True)
    description_en = models.TextField(_("Описание_en"), blank=True, null=True)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    is_active = models.BooleanField(_("Активность"), default=True)

    def __str__(self):
        return self.name

    def trans_field(self, exp_req, name):
        try:
            lang = exp_req.COOKIES[settings.LANGUAGE_COOKIE_NAME]
        except KeyError:
            try:
                lang = exp_req.session[settings.LANGUAGE_COOKIE_NAME]
            except KeyError:
                lang = "ru"
        if lang is None:
            lang = "ru"

        return getattr(self, name + "_" + lang, None)

    class Meta:
        abstract = True
        ordering = ("sort",)
