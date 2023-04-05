from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

exposed_request = ''

class List(models.Model):
    name_ru = models.CharField(_("Наименование"), max_length=128)
    name_en = models.CharField(_("Наименование"), max_length=128)
    description_ru = models.TextField(_("Описание_ru"), blank=True, null=True)
    description_en = models.TextField(_("Описание_en"), blank=True, null=True)
    is_active = models.BooleanField(_("Активность Системы"), default=True)

    @property
    def name(self):
        try:
            lang = exposed_request.session[settings.LANGUAGE_SESSION_KEY]
        except KeyError:
            try:
                lang = exposed_request.session[settings.LANGUAGE_COOKIE_NAME]
            except KeyError:
                lang = 'ru'
        return getattr(self, 'name_'+lang, None)

    @property
    def description(self):
        try:
            lang = exposed_request.session[settings.LANGUAGE_SESSION_KEY]
        except KeyError:
            try:
                lang = exposed_request.session[settings.LANGUAGE_COOKIE_NAME]
            except KeyError:
                lang = 'ru'
        #print('exposed_request:', exposed_request, lang, 'title_'+lang)
        return getattr(self, 'description_'+lang, None)

    def __str__(self):
        return (self.datecreate.strftime('%d.%m.%Y %H:%M:%S') + '|' + self.name)