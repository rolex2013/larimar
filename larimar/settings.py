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

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@2%zg8-cp_cqq!=4g-1o0ok6#q3t##0a3@hrat-=i8(=!7(xr!'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = False

#INTERNAL_IPS = [
#    '127.0.0.1',
#    '192.168.88.153',
#]

ADMINS = (('Harry', 'larimaritgroup.ru@gmail.com'),)

# Application definition

INSTALLED_APPS = [
    'debug_toolbar',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jquery',
    'bootstrap4',
    'crispy_forms',
    'bootstrap_datepicker_plus',
    #'bootstrap4_datetime',
    'django_mptt_admin',
    'mptt',
    'ckeditor',
    'ckeditor_uploader',
    'django_tables2',
    'menu',
    'accounts',
    'main', 
    'companies',
    'finance', 
    'projects',
    'crm',
]

BOOTSTRAP4 = {
    'include_jquery': True,
}

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'larimar.urls'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CKEDITOR_UPLOAD_PATH = "uploads/"

#CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default': {
       'toolbar': 'None'
    },
}

#CKEDITOR_CONFIGS = {
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
#}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'larimar.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_HOST = 'smtp.beget.com'
EMAIL_PORT = 2525
EMAIL_HOST_USER = "1yes@larimaritgroup.ru"
EMAIL_HOST_PASSWORD = "CucumbeR---000"
EMAIL_USE_TLS = False
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/



if sys.platform == "win32":
   # для разработки

   DEBUG = True
   INTERNAL_IPS = [
       '127.0.0.1',
       '192.168.88.153',
   ]

   STATIC_URL = '/static/'
   STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  

   ALLOWED_HOSTS = ['localhost','192.168.88.153']

   # Database
   # https://docs.djangoproject.com/en/3.0/ref/settings/#databases

   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
       }
   }

   def show_toolbar(request):
      return True

   DEBUG_TOOLBAR_CONFIG = {
     "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
   }

else:

   ALLOWED_HOSTS = ['1yes.larimaritgroup.ru']

   STATIC_URL = '/larimar/static/'
   STATICFILES_DIRS = ('/home/l/larimarit/1yes.larimaritgroup.ru/public_html/larimar/static',)
   STATIC_ROOT = '/home/l/larimarit/1yes.larimaritgroup.ru/public_html/larimar/static/static_collected'

   DATABASES = {
      'default': {
         #'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'ENGINE': 'django.db.backends.mysql',
         'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
         'NAME': 'larimarit_1yes',
         'USER': 'larimarit_1yes',
         'PASSWORD': 'CucumbeR@000',
         'HOST': '127.0.0.1',
         #'PORT': '5432'
         'PORT': '3306'
      }
   }

