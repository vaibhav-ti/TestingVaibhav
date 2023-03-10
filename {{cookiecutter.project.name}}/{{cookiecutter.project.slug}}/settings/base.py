"""
Django settings for {{cookiecutter.project.slug}} project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from decouple import config
import os
from pathlib import Path
{% if cookiecutter.configuration.xray.enabled == "True" %}
from aws_xray_sdk import global_sdk_config

global_sdk_config.set_sdk_enabled(config("AWS_XRAY_SDK_ENABLED", default=False, cast=bool))
{% endif %}
{% if cookiecutter.configuration.logger.enabled == "True" %}
from .logger import *
{% endif %}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default="django-insecure-976gl!=dg_9^upz%)7mbgzi78@d&nprrwk38psuh&zb_716cwn")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django_extensions',
    {%- if cookiecutter.configuration.xray.enabled == 'True' and cookiecutter.deployment.selected != 'EYK' %}
    'aws_xray_sdk.ext.django',
    {%- endif %}

    'rest_framework',
    {%- if cookiecutter.authentication.rest.enabled == 'True' %}
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    {%- endif %}
    {%- if cookiecutter.authentication.rest.enabled == 'True' or cookiecutter.authentication.social.enabled == 'True' %}
    'allauth',
    'allauth.account',
    {%- endif %}

    {%- if cookiecutter.authentication.social.enabled == 'True' %}
    'allauth.socialaccount',
    'social_django',
    'rest_social_auth',
    {% endif %}
    'corsheaders',
    
    {%- if cookiecutter.documentation.swagger.enabled == 'True' %}
    'drf_yasg',
    {% endif %}
    # 'health_check',
    
    "accounts",
]

MIDDLEWARE = [
    {%- if cookiecutter.configuration.xray.enabled == 'True' and cookiecutter.deployment.selected != 'EYK' %}
    'aws_xray_sdk.ext.django.middleware.XRayMiddleware',
    {%- endif %}
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.disable_csrf.DisableCSRF',
]

ROOT_URLCONF = '{{cookiecutter.project.slug}}.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = '{{cookiecutter.project.slug}}.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_ALLOW_ALL = True
AUTH_USER_MODEL = "accounts.User"
SITE_ID = 1

{%- if cookiecutter.authentication.enabled == 'True' %}
# ---- allauth and rest-auth settings ----
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'

AUTHENTICATION_BACKENDS = (
    {%- if cookiecutter.authentication.social.enabled == 'True' %}
    {%- if cookiecutter.authentication.social.google.enabled == 'True' %}
    'social_core.backends.google.GoogleOAuth2',
    {%- endif %}
    {%- if cookiecutter.authentication.social.github.enabled == 'True' %}
    'social_core.backends.github.GithubOAuth2',
    {%- endif %}
    {%- endif %}

    'django.contrib.auth.backends.ModelBackend',
    # allauth specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

{%- if cookiecutter.authentication.social.enabled == 'True' %}
{%- if cookiecutter.authentication.social.google.enabled == 'True' %}
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]
{%- endif %}
{%- if cookiecutter.authentication.social.github.enabled == 'True' %}
SOCIAL_AUTH_GITHUB_KEY = config('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = config('SOCIAL_AUTH_GITHUB_SECRET')
{%- endif %}

{%- if cookiecutter.authentication.social.devconnect.enabled == 'True' %}
DEVCONNECT_ISSUER_URL = config('DEVCONNECT_ISSUER_URL')
DEVCONNECT_CLIENT_ID = config('DEVCONNECT_CLIENT_ID')
DEVCONNECT_CLIENT_SECRET = config('DEVCONNECT_CLIENT_SECRET')
{%- endif %}

REST_SOCIAL_OAUTH_ABSOLUTE_REDIRECT_URI = config('REST_SOCIAL_OAUTH_ABSOLUTE_REDIRECT_URI')
{%- endif %}
{%- endif %}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DATETIME_FORMAT': "%b %d %Y %H:%M:%S",
    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle'
    # ],
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '10000/day',
    #     'user': '100000/day'
    # },
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 20
}

{% if cookiecutter.configuration.xray.enabled == 'True' and cookiecutter.deployment.selected != 'EYK' %}
XRAY_RECORDER = {
    "AWS_XRAY_DAEMON_ADDRESS": "127.0.0.1:2000",
    "AUTO_INSTRUMENT": True,
    "AWS_XRAY_CONTEXT_MISSING": "LOG_ERROR",
    "AWS_XRAY_TRACING_NAME": "{{ cookiecutter.project.name }}",
    "PATCH_MODULES": ["requests"],
    "PLUGINS": (),
    "SAMPLING": True,
    "SAMPLING_RULES": None,
    "DYNAMIC_NAMING": None,
    "STREAMING_THRESHOLD": None,
}
{% endif %}

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
