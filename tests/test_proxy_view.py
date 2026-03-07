from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_api_proxy.views import ProxyBase
from tests.utils import parametrize
from responses import matchers
import responses


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
    @parametrize('method', [('get',), ('post',), ('put',), ('patch',),
                            ('delete',), ('head',), ('options',), ('trace',),])
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
    @parametrize('header,value', [('Authorization', 'token 123'),
                                  ('Accept', 'application/json'),
                                  ('Custom', 'xyz'), ])
    def test_forward_headers(self, header, value):
        responses.add(
            responses.GET,
            test_url,
            match=[matchers.header_matcher({header: value})],
            status=200,
        )

        # Django will change the request headers according to:
        # https://docs.djangoproject.com/en/6.0/ref/request-response/#django.http.HttpRequest.META
        headers = {'HTTP_%s' % header.upper().replace('-', '_'): value}

        request = self.factory.generic(responses.GET, test_path, **headers)

        proxy = ProxyBase.as_view(
            proxy_settings=proxy_settings | {'FORWARD_HEADERS': [header]}
        )
        response = proxy(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @responses.activate
    def test_forward_unchanged_body(self):
        responses.add(
            responses.POST,
            test_url,
            match=[matchers.body_matcher('the-body')],
            status=200,
        )

        request = self.factory.generic(responses.POST, test_path, 'the-body')

        proxy = ProxyBase.as_view(proxy_settings=proxy_settings)
        response = proxy(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @responses.activate
    def test_forward_unchanged_file(self):
        file_content = b'my-master-piece-text'
        file = SimpleUploadedFile('unusual-filename.txt', file_content)

        # Matcher to check if the filename and file content are both present
        # in the received request body
        def file_matcher(request):
            tokens = [file.name.encode('utf-8'), file_content]
            received = all(token in request.body for token in tokens)
            return received, ''
        responses.post(test_url, match=[file_matcher], status=200)

        request = self.factory.post(
            test_path,
            {'file': file},
            format='multipart'
        )

        proxy = ProxyBase.as_view(proxy_settings=proxy_settings)
        response = proxy(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @responses.activate
    def test_download_in_memory_file(self):
        data = b'rocoli'

        responses.add(
            responses.GET,
            test_url,
            body=data,
            status=200,
        )

        request = self.factory.get(test_path)
        proxy = ProxyBase.as_view(proxy_settings=proxy_settings)
        response = proxy(request)

        self.assertEqual(response.content, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
