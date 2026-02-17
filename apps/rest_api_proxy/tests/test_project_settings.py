import pytest
from rest_framework.test import APITestCase
from apps.rest_api_proxy.views import ProxyBase
from django.conf import settings


class LoadSettingsTestCase(APITestCase):
    def test_load_project_settings(self):
        proxy = ProxyBase()
        self.assertEqual(proxy.proxy_host(), settings.REST_API_PROXY['HOST'])
