from django.db import models

from django.urls import reverse, reverse_lazy
from django.utils import timezone


class Dict_Currency(models.Model):
    code_char = models.CharField("Символьный код", max_length=3)
    code_num = models.CharField("Цифровой код", max_length=3)
    name = models.CharField("Наименование", max_length=64)
    shortname = models.CharField("Краткое наименование", blank=True, null=True, max_length=24)
    symbol = models.CharField("Символ", blank=True, null=True, max_length=1)    
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)    
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Вид валюты'
        verbose_name_plural = 'Виды валют'
    def __str__(self):
        return (self.name)
