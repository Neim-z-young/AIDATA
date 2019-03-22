"""
Django settings for AIdatacollect project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import platform

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2z89fq5_vax4rvjjjpu+n!*a-h^8%e)c3o18pk3n*db9&=bi20'

#with open(os.environ['HOME']+'/桌面/DjangoWebApp/myWebSecret.txt') as f:
#    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'datacollect.apps.DatacollectConfig',
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AIdatacollect.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'AIdatacollect.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if platform.system() == 'Windows':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'wordpress',
            'USER': 'tbwtbwtbw',
            'PASSWORD': 'qwertyuiop',
            'HOST': 'localhost',
            'PORT': '3306',
            'default-character-set': 'utf8',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR+'/static/'

#cunstom user path
if platform.system() == 'Windows':
    MY_USER_PATH = 'F://'
else:
    MY_USER_PATH = os.environ['HOME']
#File path to storage data
MEDIA_ROOT = MY_USER_PATH + '/datacollectStorage/media/'

MEDIA_URL = '/media/'

#Custom User model
AUTH_USER_MODEL = 'datacollect.AppUniqueUser'

#Custom Auth Backens
AUTHENTICATION_BACKENDS = [
    #'django.contrib.auth.backends.ModelBackend',
    'datacollect.customAuth.UseremailAndPasswordAuthBackend',
    'datacollect.customAuth.WechatOpenidAuthBackend',
]

#deal with warnings raised by python manage.py check --deploy
#X_FRAME_OPTIONS = "DENY"
#SECURE_CONTENT_TYPE_NOSNIFF = True
#SECURE_BROWSER_XSS_FILTER = True

#HTTPS required
#SECURE_SSL_REDIRECT = True
#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True

#Performance optimizations
CONN_MAX_AGE = 10

#session max age, try to wipe outdate user, default is two weeks
SESSION_COOKIE_AGE = 1209600