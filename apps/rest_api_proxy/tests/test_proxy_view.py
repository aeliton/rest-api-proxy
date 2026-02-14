from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from apps.rest_api_proxy.views import ProxyBase
from apps.rest_api_proxy import settings
import responses


def proxy_with_settings(proxy_settings):
    proxy = ProxyBase()
    proxy.proxy_settings = settings.RAPSettings(proxy_settings)
    return proxy


class ProxyBaseTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_proxy_url(self):
        proxy = proxy_with_settings({'HOST': 'http://test.io'})
        request = self.factory.get('/api/test/')
        self.assertEqual(proxy.proxy_url(request), 'http://test.io/api/test/')

    @responses.activate
    def test_request_proxied_service(self):
        responses.add(
            responses.GET,
            'http://test.io/api/test/',
            status=200
        )
        proxy = proxy_with_settings({'HOST': 'http://test.io'})
        request = self.factory.get('/api/test/')
        response = proxy.get(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
