from django.conf import settings
from django.db import models

from django.utils.translation import gettext_lazy as _
from main.utils_lang import TranslateFieldMixin

#from django.urls import reverse, reverse_lazy
#from django.utils import timezone

# request, пробрасываемый сюда из main\request_exposer.py
exposed_request = ''


class Dict_Currency(TranslateFieldMixin, models.Model):
    code_char = models.CharField("Символьный код", max_length=3)
    code_num = models.CharField("Цифровой код", max_length=3)
    name_ru = models.CharField(_("Наименование_ru"), max_length=64, help_text=_("Наименование валюты"))
    name_en = models.CharField(_("Наименование_en"), max_length=64, help_text=_("Наименование валюты"))
    shortname_ru = models.CharField(_("Краткое наименование_ru"), blank=True, null=True, max_length=24)
    shortname_en = models.CharField(_("Краткое наименование_en"), blank=True, null=True, max_length=24)
    symbol = models.CharField(_("Символ"), blank=True, null=True, max_length=1)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    # name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def name(self):
        # # try:
        # #     lang = exposed_request.session[settings.LANGUAGE_SESSION_KEY]
        # # except KeyError:
        # #     try:
        # #         lang = exposed_request.session[settings.LANGUAGE_COOKIE_NAME]
        # #     except KeyError:
        # #         lang = 'ru'
        # try:
        #     lang = exposed_request.COOKIES[settings.LANGUAGE_COOKIE_NAME]
        # except KeyError:
        #     try:
        #         lang = exposed_request.session[settings.LANGUAGE_COOKIE_NAME]
        #     except KeyError:
        #         lang = "ru"
        # if lang is None:
        #     lang = "ru"
        # return getattr(self, 'name_'+lang, None)
        return self.trans_field(exposed_request, "name")

    @property
    def shortname(self):
        # # try:
        # #     lang = exposed_request.session[settings.LANGUAGE_SESSION_KEY]
        # # except KeyError:
        # #     try:
        # #         lang = exposed_request.session[settings.LANGUAGE_COOKIE_NAME]
        # #     except KeyError:
        # #         lang = 'ru'
        # try:
        #     lang = exposed_request.COOKIES[settings.LANGUAGE_COOKIE_NAME]
        # except KeyError:
        #     try:
        #         lang = exposed_request.session[settings.LANGUAGE_COOKIE_NAME]
        #     except KeyError:
        #         lang = "ru"
        # if lang is None:
        #     lang = "ru"
        # return getattr(self, 'shortname_'+lang, None)
        return self.trans_field(exposed_request, "shortname")

    class Meta:
        ordering = ('sort',)
        verbose_name = _('Вид валюты')
        verbose_name_plural = _('Виды валют')

    def __str__(self):
        return (self.name)


class CurrencyRate(models.Model):
    currency = models.ForeignKey('Dict_Currency', on_delete=models.CASCADE, related_name='currencyrate_currency', verbose_name="Валюта")
    date = models.DateTimeField("Дата")
    rate = models.DecimalField("Курс", max_digits=12, decimal_places=4)
    datecreate = models.DateTimeField("Дата загрузки", auto_now_add=True)
    is_active = models.BooleanField("Активность", default=True)

    def __str__(self):
        return (self.currency.name + '. ' + self.date.strftime('%d.%m.%Y, %H:%M') + ' - ' + str(self.rate))

    class Meta:
        unique_together = ('currency','date')
        ordering = ('-date', 'currency')
        verbose_name = 'История курса валют'
        verbose_name_plural = 'Истории курсов валют'
