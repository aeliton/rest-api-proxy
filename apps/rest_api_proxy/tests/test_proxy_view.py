from .utils import parametrize
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from apps.rest_api_proxy.views import ProxyBase
import responses
from responses import matchers


test_base_url = 'http://t.io'
test_path = '/api/test'
test_url = f'{test_base_url}{test_path}'
proxy_settings = {'HOST': test_base_url}


class ProxyBaseTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_proxy_url(self):
        proxy = ProxyBase(proxy_settings=proxy_settings)
        request = self.factory.get(test_path)
        self.assertEqual(proxy.proxy_url(request), test_url)

    @responses.activate
    @parametrize('method', [("get",), ("post",), ("put",), ("patch",),
                            ("delete",), ("head",), ("options",), ("trace",),])
    def test_base_proxy_forwards_all_methods(self, method):
        responses.add(
            method.upper(),
            test_url,
            status=200
        )
        request = self.factory.generic(method.upper(), test_path)
        proxy = ProxyBase.as_view(proxy_settings=proxy_settings)
        response = proxy(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @responses.activate
    @parametrize('header,value', [("Authorization", "token 123"),
                                  ("Accept", "application/json"),
                                  ("Custom", "xyz"), ])
    def test_forward_headers(self, header, value):
        responses.add(
            responses.GET,
            test_url,
            match=[matchers.header_matcher({header: value})],
            status=200,
        )

        # Django will change the request headers according to:
        # https://docs.djangoproject.com/en/6.0/ref/request-response/#django.http.HttpRequest.META
        headers = {'HTTP_%s' % header.upper().replace("-", "_"): value}

        request = self.factory.generic(responses.GET, test_path, **headers)

        proxy = ProxyBase.as_view(proxy_settings=proxy_settings)
        response = proxy(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
