from django.conf import settings
from django.db import models

from django.utils.translation import gettext_lazy as _

# from main.utils_lang import TranslateFieldMixin
from main.utils_model import Dict_Model

# from django.urls import reverse, reverse_lazy
# from django.utils import timezone

# request, пробрасываемый сюда из main\request_exposer.py


exposed_request = ""


class Dict_Currency(Dict_Model):
    code_char = models.CharField("Символьный код", max_length=3)
    code_num = models.CharField("Цифровой код", max_length=3)
    shortname_ru = models.CharField(
        _("Краткое наименование_ru"), blank=True, null=True, max_length=24
    )
    shortname_en = models.CharField(
        _("Краткое наименование_en"), blank=True, null=True, max_length=24
    )
    symbol = models.CharField(_("Символ"), blank=True, null=True, max_length=1)

    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    @property
    def shortname(self):
        return self.trans_field(exposed_request, "shortname")

    class Meta:
        verbose_name = _("Вид валюты")
        verbose_name_plural = _("Виды валют")


class CurrencyRate(models.Model):
    currency = models.ForeignKey(
        "Dict_Currency",
        on_delete=models.CASCADE,
        related_name="currencyrate_currency",
        verbose_name="Валюта",
    )
    date = models.DateTimeField("Дата")
    rate = models.DecimalField("Курс", max_digits=12, decimal_places=4)
    datecreate = models.DateTimeField("Дата загрузки", auto_now_add=True)
    is_active = models.BooleanField("Активность", default=True)

    def __str__(self):
        return (
            self.currency.name
            + ". "
            + self.date.strftime("%d.%m.%Y, %H:%M")
            + " - "
            + str(self.rate)
        )

    class Meta:
        unique_together = ("currency", "date")
        ordering = ("-date", "currency")
        verbose_name = "История курса валют"
        verbose_name_plural = "Истории курсов валют"
