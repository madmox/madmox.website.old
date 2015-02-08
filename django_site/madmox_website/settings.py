"""
Django settings for madmox_website project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
import sys
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from core.tools import get_env_var

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# General settings

SECRET_KEY = get_env_var('DJANGO_SECRET_KEY', required=False, default='')
DEBUG = (get_env_var('DJANGO_DEBUG', required=False) != None)
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = get_env_var('DJANGO_ALLOWED_HOSTS').split()
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = '/'
RUNNING_DEVSERVER = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')

# Emailing

ADMINS = tuple(get_env_var('DJANGO_ADMINS', required=False, default='').split())
EMAIL_HOST = get_env_var('DJANGO_EMAIL_HOST', required=False, default='localhost')
EMAIL_PORT = int(get_env_var('DJANGO_EMAIL_PORT', required=False, default='25'))
EMAIL_HOST_USER = get_env_var('DJANGO_EMAIL_HOST_USER', required=False, default='')
EMAIL_HOST_PASSWORD = get_env_var('DJANGO_EMAIL_HOST_PASSWORD', required=False, default='')
SERVER_EMAIL = get_env_var('DJANGO_SERVER_EMAIL', required=False, default='root@localhost')

# Application definition

DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
)

LOCAL_APPS = (
    'core',
    'accounts',
    'about',
    'recipes',
    'shatterynote',
    'share',
)

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    "django.core.context_processors.request",
    "core.context_processors.piwik",
)

ROOT_URLCONF = 'madmox_website.urls'

WSGI_APPLICATION = 'madmox_website.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_var('DJANGO_DATABASE_NAME'),
        'USER': get_env_var(
            'DJANGO_DATABASE_USER', required=False, default=''
        ),
        'PASSWORD': get_env_var(
            'DJANGO_DATABASE_PASSWORD', required=False, default=''
        ),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'fr-FR'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = get_env_var('DJANGO_STATIC_ROOT', required=False)
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# User-uploaded files
MEDIA_ROOT = get_env_var('DJANGO_MEDIA_ROOT')
MEDIA_URL = '/media/'
