# This is a minimal django application to demonstrate how an interceptor
# can be implemented for django. Use this at your own risk.
from pathlib import Path
from django.core.management.utils import get_random_secret_key
from cryptography.fernet import Fernet

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = get_random_secret_key()

DEBUG = True

ALLOWED_HOSTS = ['cipher']

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
]

ROOT_URLCONF = "cipher_proxy.urls"

WSGI_APPLICATION = "cipher_proxy.wsgi.application"

DATABASES = {
}

################################################################################
# rest_api_proxy configuration
REST_API_PROXY = {
    'HOST': 'http://backend:8080',
}

# encryption/description key
CIPHER_KEY = Fernet.generate_key()
################################################################################
