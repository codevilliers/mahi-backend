"""
Django settings for mahi_care project.

"""

import yaml
from pathlib import Path
import firebase_admin
from firebase_admin import credentials

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Parent directory for the project
PARENT_DIR = BASE_DIR.parent

# configuration file contains configurations for the app
CONFIGURATION_FILE = open(PARENT_DIR/'configurations/base.yml')

CONFIGURATION = yaml.safe_load(CONFIGURATION_FILE)

SECRETS = CONFIGURATION['secrets']
DATABASE = CONFIGURATION['services']['database']
ENVIRONMENT = CONFIGURATION['environment']

SECRET_KEY = SECRETS['secretKey']

IS_PRODUCTION_ENV = ENVIRONMENT['production']
HOST_URL = ENVIRONMENT['hostURL']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not IS_PRODUCTION_ENV

ALLOWED_HOSTS = [HOST_URL, ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'mahi_auth.apps.MahiAuthConfig',
    'mahi_app.apps.MahiAppConfig',
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

ROOT_URLCONF = 'mahi_care.urls'

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

WSGI_APPLICATION = 'mahi_care.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DATABASE['name'],
        'USER': DATABASE['user'],
        'PASSWORD': DATABASE['password'],
        'HOST': DATABASE['host'],
        'PORT': DATABASE['port']
    }
}

AUTH_USER_MODEL = 'mahi_auth.User'

AUTHENTICATION_BACKENDS = [
    'mahi_auth.backends.auth_backend.MahiAuthBackend',
]

# Password validation

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

# TODO: Use cached sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

SESSION_COOKIE_NAME = 'mahi_session'

CSRF_COOKIE_NAME = 'mahi_csrftoken'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25
}

# Initialize firebase
cred = credentials.Certificate(
    str(PARENT_DIR/'configurations/mahi_firebase.json')
)
firebase_admin.initialize_app(cred)

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static_files/'
STATIC_ROOT = PARENT_DIR/'static_files'

# Media files

MEDIA_URL = '/media/'

MEDIA_ROOT = PARENT_DIR/'media_files'
