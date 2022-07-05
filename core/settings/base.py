from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

import sys
from os.path import abspath, basename, dirname, join, normpath

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# fetch Django's project directory
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# fetch the project_root
PROJECT_ROOT = dirname(DJANGO_ROOT)

# the name of the whole site
SITE_NAME = basename(DJANGO_ROOT)

# collect static files here
STATIC_ROOT = join(
    PROJECT_ROOT,
    "run",
    "static",
)

# look for templates here
# This is an internal setting, used in the TEMPLATES directive
PROJECT_TEMPLATES = join(
    PROJECT_ROOT,
    "templates",
)

# leading slash
APPEND_SLASH = False

# collect media files here
MEDIA_ROOT = join(
    PROJECT_ROOT,
    "run",
    "media",
)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# the URL for static files
STATIC_URL = "/static/"

# the URL for media files
MEDIA_URL = "/media/"

SECRET_FILE = normpath(
    join(
        PROJECT_ROOT,
        "run",
        "SECRET.key",
    )
)

# add
sys.path.append(
    normpath(
        join(
            PROJECT_ROOT,
            "apps",
        )
    )
)


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = [
    "games",
    "users",
    "cart",
    "chat",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "drf_yasg",
    "rest_framework_simplejwt",
    "rest_framework.authtoken",
    "django_filters",
    "djmoney",
    "channels",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.steam",
]

INSTALLED_APPS = INSTALLED_APPS + LOCAL_APPS + THIRD_PARTY_APPS

ROOT_URLCONF = "core.urls"

# the default ASGI application
ASGI_APPLICATION = "%s.asgi.application" % SITE_NAME

# the default WSGI application
WSGI_APPLICATION = "%s.wsgi.application" % SITE_NAME

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_TEMPLATES],
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


# Password validation
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

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        # Django imports
        from django.utils.crypto import get_random_string

        chars = "abcdefghijklmnopqrstuvwxyz0123456789!$%&()=+-_"
        SECRET_KEY = get_random_string(
            50,
            chars,
        )
        with open(
            SECRET_FILE,
            "w",
        ) as f:
            f.write(SECRET_KEY)
    except IOError:
        raise Exception("Could not open %s for writing!" % SECRET_FILE)
