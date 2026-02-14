from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from apps.rest_api_proxy.views import ProxyBase
import responses


test_base_url = 'http://t.io'
test_path = '/api/test'
test_url = f'{test_base_url}{test_path}'


class ProxyBaseTestCase(APITestCase):
    def setUp(self):
        self.proxy = ProxyBase({'HOST': test_base_url})
        self.factory = APIRequestFactory()

    def test_proxy_url(self):
        request = self.factory.get(test_path)
        self.assertEqual(self.proxy.proxy_url(request), test_url)

    @responses.activate
    def test_request_proxied_service(self):
        responses.add(
            responses.GET,
            test_url,
            status=200
        )
        request = self.factory.get(test_path)
        response = self.proxy.get(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
