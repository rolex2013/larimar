# -*- coding: utf-8 -*-

from modeltranslation.translator import translator, TranslationOptions
from .models import Dict_Currency

class Dict_CurrencyTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели Dict_Currency.
    """

    fields = ('name',)

translator.register(Dict_Currency, Dict_CurrencyTranslationOptions)