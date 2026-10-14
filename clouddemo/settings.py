"""Minimal Django settings for a Laravel Cloud test deployment."""
import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Set DJANGO_SECRET_KEY in Laravel Cloud environment variables.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "insecure-local-dev-key-change-me")
DEBUG = os.environ.get("DJANGO_DEBUG", "false").lower() == "true"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")
CSRF_TRUSTED_ORIGINS = os.environ.get(
    "DJANGO_CSRF_TRUSTED_ORIGINS", "https://*.laravel.cloud"
).split(",")

# Laravel Cloud terminates HTTPS at its proxy.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "clouddemo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "clouddemo.wsgi.application"

# Laravel Cloud injects DATABASE_URL when a database is attached.
# Without it, a local SQLite file is used (fine locally, NOT persistent on Cloud).
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Laravel Cloud provides STATIC_ROOT and STATIC_URL; Nginx serves /static/.
STATIC_ROOT = os.environ.get("STATIC_ROOT", BASE_DIR / "staticfiles")
STATIC_URL = os.environ.get("STATIC_URL", "/static/")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Send logs to stdout so they show in the Laravel Cloud Logs tab.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
