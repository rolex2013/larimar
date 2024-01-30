# перенесено в utils_model.py

from django.conf import settings

# exposed_request = ''


class TranslateFieldMixin(object):
    model = None
    model_form = None
    template = None

    def trans_field(self, exposed_request, name):
        # try:
        #     lang = exposed_request.session[settings.LANGUAGE_COOKIE_NAME]
        # except KeyError:
        #     lang = 'ru'
        # lang = exposed_request.session[settings.LANGUAGE_SESSION_KEY]
        # print("**********************", exposed_request)

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
