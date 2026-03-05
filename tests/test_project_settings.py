from rest_framework.test import APITestCase
from rest_api_proxy.views import ProxyBase


class LoadSettingsTestCase(APITestCase):
    def test_load_project_settings(self):
        proxy = ProxyBase()
        self.assertEqual(proxy.proxy_host(), 'http://from-settings.test')
