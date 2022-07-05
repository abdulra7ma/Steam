from .base import *
from .drf import *

SITE_ID = 1

AUTH_USER_MODEL = "users.User"

USER_ONLINE_TIMEOUT = 300


# #####  DATABASE CONFIGURATION ############################
DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.postgresql",
    #     "NAME": "huilo",
    #     "USER": "khasan",
    #     "PASSWORD": "1",
    #     "HOST": "localhost",
    #     "PORT": 5432,
    # }
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": join(PROJECT_ROOT, "run", "dev.sqlite3"),
    }
}

# #####  EMAIL CONFIGURATION ############################
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "hasan.ucuturkiye@gmail.com"
EMAIL_HOST_PASSWORD = "svwfejmewyrtpfge"

# #####  CELERY CONFIGURATION ############################
BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Bishkek"

# ##### AUTHENTICATION CONFIGURATION ############################
AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        "APP": {"client_id": "123", "secret": "456", "key": ""}
    }
}

# #####  DJANGO MONEY CONFIGURATION ############################
CURRENCIES = ("USD", "EUR")
CURRENCY_CHOICES = [("USD", "USD $"), ("EUR", "EUR C")]

# #####  DJANGO CHANNELS CONFIGURATION ############################
CHANNEL_LAYERS = {
    "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
}
