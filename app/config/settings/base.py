"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import importlib
import json
import numbers
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import raven
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = os.path.dirname(BASE_DIR)
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# static
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_DIR,
]

# secret
SECRET_DIR = os.path.join(ROOT_DIR, '.secrets')
SECRET_BASE = os.path.join(SECRET_DIR, 'base.json')
SECRET_LOCAL = os.path.join(SECRET_DIR, 'local.json')
SECRET_DEV = os.path.join(SECRET_DIR, 'dev.json')
SECRET_PRODUCTION = os.path.join(SECRET_DIR, 'production.json')

secrets = json.loads(open(SECRET_BASE, 'rt').read())


def set_config(obj, module_name=None, start=False):
    def eval_obj(obj):

        # 객체가 int, float거나
        if isinstance(obj, numbers.Number) or (
                # srt형이면서 숫자 변환이 가능한 경우
                isinstance(obj, str) and obj.isdigit()):
            return obj

        # 객체가 int, float가 아니면서 숫자형태를 가진 str도 아닐경우
        try:
            return eval(obj)
        except NameError:
            # 없는 변수를 참조할때 발생하는 에러
            return obj
        except Exception as e:
            print(f'Cannot eval object({obj}), Exception: {e}')
            return obj

    # base.json파일을 partsing한 결과 (python dict)를 순회
    # set_config에 전달된 개게가 'dict'형태일 경우
    if isinstance(obj, dict):
        for key, value in obj.items():
            # value가 dict거나 list일 경우 재귀적으로 함수를 다시 실행
            if isinstance(value, dict) or isinstance(value, list):
                set_config(value)
            # 그 외의 경우 value를 평가한 값을 할당
            else:
                obj[key] = eval_obj(value)
            # set_config()가 처음 호출된 loop에서만 setattr()을 실행
            if start:
                setattr(sys.modules[module_name], key, value)

    # 전달된 객체가 'list' 형태일 경우
    elif isinstance(obj, list):
        # list 아이템을 순회하며
        for index, item in enumerate(obj):
            # list의 해당 index 에 item을 평가한 값을 할당
            obj[index] = eval_obj(item)


# set_config에서 'raven' 모듈을 필요로 하나, 이 모듈의 다른 부분에서 사용하지 않음
# import raven이라고 쓸 경우 Code reformating에서 필요없는 import로 인식해서 지워짐
# raven 모듈을 importlib을 사용해 가져온 후 현재 모듈에 'raven'이라는 이름으로 할당
setattr(sys.modules[__name__], 'raven', importlib.import_module('raven'))
set_config(secrets, module_name=__name__, start=True)

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'members.User'

CORS_ORIGIN_WHITELIST = (
    'localhost:4200',
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    'raven.contrib.django.raven_compat',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    'members',
    'utils',
    'address.apps.AddressConfig',
    'restaurant.apps.RestaurantConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATES_DIR,
        ],
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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',  # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

# GEOIP
GEOIP_PATH = os.path.join(BASE_DIR, 'GEOIP')

# REST FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
}
