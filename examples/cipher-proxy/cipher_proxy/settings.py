# This is a minimal django application to demonstrate how an interceptor
# can be implemented for django. Use this at your own risk.
from pathlib import Path
from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = get_random_secret_key()

DEBUG = True

ALLOWED_HOSTS = []

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
    'HOST': 'http://127.0.0.1:8000',
}

# encryption/decription key
CIPHER_KEY = b'Xq-1c8C_yd4PepR_PofObx251YdzqM9-QUiI3I7ajzc='
################################################################################
