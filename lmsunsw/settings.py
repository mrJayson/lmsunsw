"""
Django settings for lmsunsw project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '__-*0p(yvr=tgqny@l-459y@f68bjtre9kddy@gopn+l!iad#l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']

# all login_required views redirect to this url
LOGIN_URL = '/login'

# once logged in, redirect to this url
LOGIN_REDIRECT_URL = '/'

# Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'crispy_forms',
    'storages',
    'session_security',
    'autoslug',
    'password_reset',
    'debug_toolbar',

)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'app.middleware.SessionSecurityMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'lmsunsw.urls'

WSGI_APPLICATION = 'lmsunsw.wsgi.application'

# Specify the default test runner.
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Caching for performance boost

#CACHE = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#        'LOCATION': 'cache_table',
#    }
#}
if 'CACHE_LOCATION' in os.environ:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': os.environ['CACHE_LOCATION'],

        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases


if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
}


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Australia/Sydney'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# media files (png)

MEDIA_ROOT = os.path.join(
                  os.path.dirname(
                      os.path.dirname(
                          os.path.abspath(__file__)
                      )
                  ),
                  'media'
              )

MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.join(
                  os.path.dirname(
                      os.path.dirname(
                          os.path.abspath(__file__)
                      )
                  ),
                  'static'
              )

STATIC_URL = '/static/'

STATICFILE_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriedFinder',
)

# Template files (html)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, 'app/templates'),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'app.context_processors.django_sessions',
    'app.context_processors.get_confidence_meter_values',
    'app.context_processors.currents',
    'app.context_processors.app_list',
    )

# Session security

SESSION_SECURITY_WARN_AFTER = 3300
SESSION_SECURITY_EXPIRE_AFTER = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Email settings

EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_HOST_USER = 'jasonhuang.2014@outlook.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = '587'
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = 'jasonhuang.2014@outlook.com'

# Code Snippet settings

LANGUAGE_CHOICES = (
    ('as3','as3'),
    ('bash','bash'),
    ('c','c'),
    ('cpp','cpp'),
    ('csharp','csharp'),
    ('css','css'),
    ('html','html'),
    ('java','java'),
    ('js','js'),
    ('make','make'),
    ('objective-c','objective-c'),
    ('perl','perl'),
    ('php','php'),
    ('python','python'),
    ('sql','sql'),
    ('ruby','ruby'),
    ('vb.net','vb.net'),
    ('xml','xml'),
    ('xslt','xslt'),
)

DEFAULT_LANGUAGE = 'c'


