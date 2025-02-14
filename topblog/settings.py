# mypy: ignore-errors
import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "DSAmdU3H783hs8M9S30k9xSi9d3KD")

DEBUG = bool(int(os.getenv("DJANGO_DEBUG", 1)))
DEVELOPMENT = bool(int(os.getenv("DJANGO_DEVELOPMENT", 1)))

REDIS_HOST = str(os.getenv("REDIS_HOST", "redis"))
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

ALLOWED_HOSTS = [
    os.getenv("ALLOWED_HOST", "*"),
]

DATABASES = {
    "default": {
        "ENGINE": os.getenv("POSTGRES_ENGINE", "django.db.backends.sqlite3"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "NAME": os.getenv("POSTGRES_DB", BASE_DIR / "db.sqlite3"),
    }
}

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "channels",
    "core",
    "chat",
    "tailwind",
    "theme",
    "users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "topblog.urls"
AUTH_USER_MODEL = "users.User"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates/"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "topblog.wsgi.application"
ASGI_APPLICATION = "topblog.asgi.application"


if DEVELOPMENT:
    CHANNEL_LAYERS = {
        "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
    }
else:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [(REDIS_HOST, REDIS_PORT)],
            },
        },
    }


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = False

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "topblog/static"),
    ]


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

NPM_BIN_PATH = "/usr/local/bin/npm"

TAILWIND_APP_NAME = "theme"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(BASE_DIR, "site_cache"),
    }
}

CSRF_TRUSTED_ORIGINS = []
if csrf_subdomain := os.getenv("CSRF_SUBDOMAIN"):
    CSRF_TRUSTED_ORIGINS += [
        f"http://{csrf_subdomain}",
        f"https://{csrf_subdomain}",
    ]

if DEBUG:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
else:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
