"""
Django settings for larimar project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
import logging
import datetime

from dotenv import load_dotenv, find_dotenv

from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language_info

import pymysql

# from django.utils.translation import gettext as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# print(BASE_DIR)

load_dotenv(BASE_DIR + "/larimar/config/.env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

ADMINS = ((os.getenv("ADMIN_NAME"), os.getenv("ADMIN_EMAIL")),)

# Application definition

INSTALLED_APPS = [
    "channels",
    # 'modeltranslation', #обошлись собственным middleware для проброса request'а в модели и полями @property
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "jquery",
    "bootstrap4",
    "crispy_forms",
    # "bootstrap_datepicker_plus",
    # 'bootstrap4_datetime',
    "django_mptt_admin",
    "mptt",
    "ckeditor",
    "ckeditor_uploader",
    "django_ckeditor_5",
    "django_tables2",
    "rest_framework",
    "rosetta",
    # 'menu',
    "accounts",
    "main",
    "companies",
    "finance",
    "projects",
    "crm",
    "docs",
    "files",
    "feedback",
    "chats",
    "lists",
    "trade",
    "dashboard",
]

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
    ),
}

# CORS_ORIGIN_WHITELIST = ('localhost:8000',)

BOOTSTRAP4 = {
    "include_jquery": True,
}

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # add our middleware for redirect user
    "accounts.middleware.LocaleMiddleware",
    "main.request_exposer.RequestExposerMiddleware",
    "companies.request_exposer.RequestExposerMiddleware",
    "finance.request_exposer.RequestExposerMiddleware",
    "lists.request_exposer.RequestExposerMiddleware",
    "docs.request_exposer.RequestExposerMiddleware",
    "files.request_exposer.RequestExposerMiddleware",
    "crm.request_exposer.RequestExposerMiddleware",
    "projects.request_exposer.RequestExposerMiddleware",
    "feedback.request_exposer.RequestExposerMiddleware",
    "chats.request_exposer.RequestExposerMiddleware",
    "dashboard.request_exposer.RequestExposerMiddleware",
]

ROOT_URLCONF = "larimar.urls"

CRISPY_TEMPLATE_PACK = "bootstrap4"

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CKEDITOR_UPLOAD_PATH = "uploads/"

# CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "None",
        # 'height': 500,
        "width": "100%"
        # 'toolbarCanCollapse': False,
        # 'forcePasteAsPlainText': True
    },
}

# CKEDITOR_CONFIGS = {
#    "default": {
#        "removePlugins": "stylesheetparser",
#        'allowedContent': True,
#        'toolbar_Full': [
#           ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat' ],
#           ['Image', 'Flash', 'Table', 'HorizontalRule'],
#           ['TextColor', 'BGColor'],
#           ['Smiley','sourcearea', 'SpecialChar'],
#           [ 'Link', 'Unlink', 'Anchor' ],
#           [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl', 'Language' ],
#           [ 'Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates' ],
#           [ 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo' ],
#           [ 'Find', 'Replace', '-', 'SelectAll', '-', 'Scayt' ],
#           [ 'Maximize', 'ShowBlocks' ]
#        ],
#    }
# }

# customColorPalette = [
#         {
#             'color': 'hsl(4, 90%, 58%)',
#             'label': 'Red'
#         },
#         {
#             'color': 'hsl(340, 82%, 52%)',
#             'label': 'Pink'
#         },
#         {
#             'color': 'hsl(291, 64%, 42%)',
#             'label': 'Purple'
#         },
#         {
#             'color': 'hsl(262, 52%, 47%)',
#             'label': 'Deep Purple'
#         },
#         {
#             'color': 'hsl(231, 48%, 48%)',
#             'label': 'Indigo'
#         },
#         {
#             'color': 'hsl(207, 90%, 54%)',
#             'label': 'Blue'
#         },
#     ]

#   CKEDITOR_5_CUSTOM_CSS = 'path_to.css' # optional
#   CKEDITOR_5_FILE_STORAGE = "path_to_storage.CustomStorage" # optional
#   CKEDITOR_5_CONFIGS = {
#     'default': {
#         'toolbar': ['heading', '|', 'bold', 'italic', 'link',
#                     'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],

#     },
#     'extends': {
#         'blockToolbar': [
#             'paragraph', 'heading1', 'heading2', 'heading3',
#             '|',
#             'bulletedList', 'numberedList',
#             '|',
#             'blockQuote',
#         ],
#         'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
#         'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
#                     'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
#                     'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
#                     'insertTable',],
#         'image': {
#             'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
#                         'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
#             'styles': [
#                 'full',
#                 'side',
#                 'alignLeft',
#                 'alignRight',
#                 'alignCenter',
#             ]

#         },
#         'table': {
#             'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
#             'tableProperties', 'tableCellProperties' ],
#             'tableProperties': {
#                 'borderColors': customColorPalette,
#                 'backgroundColors': customColorPalette
#             },
#             'tableCellProperties': {
#                 'borderColors': customColorPalette,
#                 'backgroundColors': customColorPalette
#             }
#         },
#         'heading' : {
#             'options': [
#                 { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
#                 { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
#                 { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
#                 { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
#             ]
#         }
#     },
#     'list': {
#         'properties': {
#             'styles': 'true',
#             'startIndex': 'true',
#             'reversed': 'true',
#         }
#     }
# }

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "larimar.wsgi.application"
# ASGI_APPLICATION = 'larimar.routing.application'
ASGI_APPLICATION = "larimar.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        # 'BACKEND': 'asgiref.inmemory.ChannelLayer',
        "BACKEND": "channels.layers.InMemoryChannelLayer",
        # 'ROUTING': 'larimar.routing.channel_routing',
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
        # 'CONFIG': {
        #     "hosts": [('127.0.0.1', 6379)],
        # },
    },
}

CELERYBEAT_SCHEDULE = {
    "prune-presence": {
        "task": "channels_presence.tasks.prune_presences",
        "schedule": datetime.timedelta(seconds=60),
    },
    "prune-rooms": {
        "task": "channels_presence.tasks.prune_rooms",
        "schedule": datetime.timedelta(seconds=600),
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
# https://vivazzi.pro/it/translate-django/
LANGUAGE_CODE = os.getenv("LANGUAGE_CODE")
LANGUAGES = [
    ("ru", _("Russian")),
    ("en", _("English")),
    # ('es', _('Spain')),
]

USE_I18N = True  # bool(os.getenv('USE_I18N', default=True))   # активация системы перевода django
USE_L10N = True  # форматирование дат и чисел в зависимости от локализации
LANGUAGE_SESSION_KEY = "session_language"
LANGUAGE_COOKIE_NAME = "cookie_language"
# месторасположение файлов перевода
LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
    os.path.join(BASE_DIR, "accounts/locale"),
    os.path.join(BASE_DIR, "finance/locale"),
)
# print('==================>', get_language_info('ru'))
TIME_ZONE = os.getenv("TIME_ZONE")
USE_TZ = bool(os.getenv("USE_TZ", default=True))


EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = bool(os.getenv("EMAIL_USE_TLS", default="False"))
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DATA_UPLOAD_MAX_NUMBER_FIELDS = None

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

GOOGLE_RECAPTCHA_SECRET_KEY = os.getenv("GOOGLE_RECAPTCHA_SECRET_KEY")

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# IS_DEV = bool(os.getenv("IS_DEV", default="False"))
IS_DEV = os.getenv("IS_DEV")

# if sys.platform == "win32":
if IS_DEV == "True":
    # для разработки

    DEBUG = True
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

    STATIC_URL = "/static/"
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
    STATIC_ROOT = os.getenv("STATIC_ROOT")

    INTERNAL_IPS = [
        "localhost",
        "127.0.0.1",
        "192.168.88.55",
    ]

    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "192.168.88.55"]

    # Database
    # https://docs.djangoproject.com/en/3.0/ref/settings/#databases

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db_test.sqlite3"),
            # "NAME": os.path.join(BASE_DIR, "data.sqlite"),
        }
    }

    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }

else:
    ALLOWED_HOSTS = [
        "larimaritgroup.ru",
        "www.larimaritgroup.ru",
        "1yes.larimaritgroup.ru",
        "www.1yes.larimaritgroup.ru",
    ]

    STATIC_URL = os.getenv("STATIC_URL")
    STATICFILES_DIRS = (os.getenv("STATICFILES_DIRS"),)
    STATIC_ROOT = os.getenv("STATIC_ROOT")

    # подменяем MySQLdb версией 1.4.6 модуля pymysql
    pymysql.version_info = (1, 4, 6, "final", 0)
    pymysql.install_as_MySQLdb()
    # ***

    DATABASES = {
        "default": {
            #'ENGINE': 'django.db.backends.postgresql_psycopg2',
            "ENGINE": "django.db.backends.mysql",
            "OPTIONS": {
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
                "charset": "utf8mb4",
                # "cursorclass": "pymysql.cursors.DictCursor",
            },
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": int(os.getenv("DB_PORT")),
        }
    }

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)
