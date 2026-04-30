import os

try:
    from decouple import config
except ImportError:
    def config(key, default=None, cast=None):
        value = os.getenv(key, default)
        if cast and value is not None:
            return cast(value)
        return value

from .base import *

SECRET_KEY = config("SECRET_KEY", default="django-insecure-local-dev-key-change-me")
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

CHANNEL_LAYERS = {
    "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"},
}
