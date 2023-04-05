from django.conf import settings

#exposed_request = ''

class TranslateFieldMixin(object):
    model = None
    model_form = None
    template = None

    def trans_field(self, exposed_request, name):
        #print('exposed_request = ', exposed_request)
        try:
            lang = exposed_request.session[settings.LANGUAGE_SESSION_KEY]
        except KeyError:
            try:
                lang = exposed_request.session[settings.LANGUAGE_COOKIE_NAME]
            except KeyError:
                lang = 'ru'
        return getattr(self, name+'_'+lang, None)