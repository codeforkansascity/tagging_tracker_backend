"""
Django settings for tagging_tracker project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import json
import os

import requests

from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True if os.environ.get("DEBUG") else False
DISABLE_AUTH = os.getenv("DISABLE_AUTH", False)

if DEBUG:
    SECRET_KEY = 'mysecretkey'
else:
    SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = [
    '52.173.204.52',
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    'tagtracker.centralus.cloudapp.azure.com',
    os.getenv('DEPLOYED_URL', ''),
    os.getenv('LOADBALANCER_URL', '')
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'backend',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework_jwt',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django.contrib.auth.backends.RemoteUserBackend',
]

ROOT_URLCONF = 'tagging_tracker.urls'

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

WSGI_APPLICATION = 'tagging_tracker.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME', 'dev'),
        'USER': os.getenv('DB_USER', 'tag_user'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', 5432),
        'EMAIL_USE_SSL': True,
        'PASSWORD': os.getenv('DB_PASSWORD', 'somepass'),
        'OPTIONS': {
            'sslmode': os.getenv('SSL_MODE', 'disable'),
            'sslrootcert': os.getenv('SSL_ROOT_CERT', '')
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

if not DISABLE_AUTH:
    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.BasicAuthentication',
        ),
    }

if not DISABLE_AUTH:
    response = requests.get(f"https://{os.environ['AUTH0_URL']}/.well-known/jwks.json")
    jwks = response.json()
    cert = '-----BEGIN CERTIFICATE-----\n' + jwks['keys'][0]['x5c'][0] + '\n-----END CERTIFICATE-----'

    certificate = load_pem_x509_certificate(str.encode(cert), default_backend())
    publickey = certificate.public_key()

    JWT_AUTH = {
        'JWT_PAYLOAD_GET_USERNAME_HANDLER':
            'auth0authorization.user.jwt_get_username_from_payload_handler',
        'JWT_PUBLIC_KEY': publickey,
        'JWT_ALGORITHM': 'RS256',
        'JWT_AUDIENCE': os.environ["AUTH0_AUDIENCE"],
        'JWT_ISSUER': os.environ["AUTH0_URL"],
        'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    }


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        '': {  # 'catch all' loggers by referencing it with the empty string
            'handlers': ['console'],
            'level': os.getenv('LOG_LEVEL', 'ERROR'),
        },
    },
}
