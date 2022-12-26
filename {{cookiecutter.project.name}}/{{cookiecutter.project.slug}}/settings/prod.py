from decouple import config
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = ['*']

{%- if cookiecutter.database.enabled == 'True' %}
DATABASES = {
    'default': {
        {%- if cookiecutter.database.type == 'postgresql' %}
        'ENGINE': 'django.db.backends.postgresql',
        {%- elif cookiecutter.database.type == 'mysql' %}
        'ENGINE': 'django.db.backends.mysql',
        {% endif %}
        'NAME': config("DB_NAME"),
        'USER': config("DB_USER"),
        'PASSWORD': config("DB_PASSWORD"),
        'HOST': config("DB_HOST"),
        'PORT': config("DB_PORT"),
    }
}
{% else %}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
{%- endif %}
{%- if cookiecutter.database.type == 'postgresql' %}
SOCIAL_AUTH_JSONFIELD_ENABLED = True
{%- endif %}

{% if cookiecutter.caching.enabled == "True" %}
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("REDIS_URL", "redis://redis:6379/0"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "",
    }
}
{% endif %}


# Storages
{%- if cookiecutter.s3.enabled == 'True' %}
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
AWS_S3_ACCESS_KEY_ID = config('AWS_S3_ACCESS_KEY_ID')
AWS_S3_SECRET_ACCESS_KEY = config('AWS_S3_SECRET_ACCESS_KEY')
AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN')
{%- endif %}
