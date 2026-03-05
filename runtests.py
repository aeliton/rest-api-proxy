#!/usr/bin/env python
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if not settings.configured:
    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"
            }
        },
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
        ],
        REST_API_PROXY={
            'HOST': 'http://from-settings.test',
        },
    )


def run_tests():
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
    sys.exit(bool(failures))


if __name__ == "__main__":
    run_tests()
