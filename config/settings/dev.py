from .base import *  # noqa: F403
from .base import MIDDLEWARE as BASE_MIDDLEWARE

DEBUG = True
ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = ["127.0.0.1"]

MIDDLEWARE = [m for m in BASE_MIDDLEWARE if "whitenoise" not in m]
STORAGES = {"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}}
