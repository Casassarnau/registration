"""
Django settings for testP project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

import dj_database_url

from .hackathon_variables import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET', ')6+vf9(1tihg@u8!+(0abk+y*#$3r$(-d=g5qhm@1&lo4pays&')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('PROD_MODE', "false").lower() == "false"
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Application definition
INSTALLED_APPS = [
    'jet',
    'jet.dashboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'form_utils',
    'bootstrap3',
    'django_tables2',
    'organizers',
    'checkin',
    'user',
    'applications',
    'teams',
    'stats',
    'storages',
    'meals',
]

if REIMBURSEMENT_ENABLED:
    INSTALLED_APPS.append('reimbursement')

if HARDWARE_ENABLED:
    INSTALLED_APPS.append('hardware')

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['app/templates', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'app.utils.hackathon_vars_processor'

            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if os.environ.get('DATABASE_URL', None):
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)

if os.environ.get('PG_PWD', None):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('PG_NAME', 'backend'),
            'USER': os.environ.get('PG_USER', 'backenduser'),
            'PASSWORD': os.environ.get('PG_PWD'),
            'HOST': os.environ.get('PG_HOST', 'localhost'),
            'PORT': '5432',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
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

# Logging config to send logs to email automatically
LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'admin_email': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'app.log.HackathonDevEmailHandler',
        },
    },
    'loggers': {
        'django': {
            'level': 'ERROR',
            'handlers': ['admin_email'],
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + '/staticfiles'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, os.path.join('app', "static")),
]
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

#  File upload configuration
MEDIA_ROOT = 'files'
MEDIA_URL = '/files/'

if os.environ.get('DROPBOX_OAUTH2_TOKEN', False):
    DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
    DROPBOX_OAUTH2_TOKEN = os.environ.get('DROPBOX_OAUTH2_TOKEN', False)
    DROPBOX_ROOT_PATH = HACKATHON_DOMAIN.replace('.', '_')

# Sendgrid API key
SENDGRID_API_KEY = os.environ.get('SG_KEY', None)

# SMTP
EMAIL_HOST = os.environ.get('EMAIL_HOST', None)
EMAIL_PORT = os.environ.get('EMAIL_PORT', None)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', None)
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', None)

# Load filebased email backend if no Sendgrid credentials and debug mode
if not SENDGRID_API_KEY and not EMAIL_HOST and DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = 'tmp/email-messages/'
else:
    if SENDGRID_API_KEY:
        EMAIL_BACKEND = "sgbackend.SendGridBackend"
    else:
        EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Jet configs
JET_SIDE_MENU_COMPACT = True
JET_INDEX_DASHBOARD = 'app.jet_dashboard.CustomIndexDashboard'

# Set up custom auth
AUTH_USER_MODEL = 'user.User'
LOGIN_URL = 'account_login'
PASSWORD_RESET_TIMEOUT_DAYS = 1

BOOTSTRAP3 = {
    # Don't normally want placeholders.
    'set_placeholder': False,
    'required_css_class': 'required',
}

if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': os.path.join(BASE_DIR, 'cache'),
        }
    }

# Add domain to allowed hosts
ALLOWED_HOSTS.append(HACKATHON_DOMAIN)

# Deployment configurations for proxy pass and csrf
CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Maximum file upload size for forms
MAX_UPLOAD_SIZE = 5242880

MEALS_TOKEN = os.environ.get('MEALS_TOKEN', None)
