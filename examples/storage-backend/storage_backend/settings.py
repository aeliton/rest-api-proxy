from pathlib import Path
from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = get_random_secret_key()

DEBUG = True

MEDIA_ROOT = '/opt/storage'

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
]

ROOT_URLCONF = "storage_backend.urls"

WSGI_APPLICATION = "storage_backend.wsgi.application"

DATABASES = {
}
