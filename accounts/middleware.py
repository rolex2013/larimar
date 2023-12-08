# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from .models import UserProfile


class LocaleMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        user = getattr(request, 'user', None)
        if not user:
            return response

        if not user.is_authenticated:
            return response

        user_lang = UserProfile.objects.filter(user=user).first().lang
        # print('middleware:', user_lang)
        if not user_lang:
            return response

        request.session[settings.LANGUAGE_SESSION_KEY] = user_lang
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_lang)

        return response