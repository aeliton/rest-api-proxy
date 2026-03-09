from rest_framework.views import APIView
from rest_api_proxy.settings import rest_api_proxy_settings, RAPSettings
from django.http import HttpHeaders, HttpResponse
import requests


class ProxyBase(APIView):
    proxy_settings: dict = None

    def __init__(self, proxy_settings=None):
        super().__init__()

        if proxy_settings:
            self.proxy_settings = RAPSettings(proxy_settings)
        else:
            self.proxy_settings = rest_api_proxy_settings

        for method in self.http_method_names:
            setattr(self, method, self.proxy)

    def proxy_host(self):
        return self.proxy_settings.HOST

    def proxy_url(self, request):
        return ''.join([self.proxy_host(), request.get_full_path()])

    def proxy(self, request, *args, **kwargs):
        headers = self._process_headers(request)
        data = self._process_data(request)
        files = self._process_files(request)
        output = requests.request(
            request.method,
            self.proxy_url(request),
            headers=headers,
            data=data,
            files=files,
        )
        response = self.process_response(output)
        if hasattr(response, 'content'):
            return HttpResponse(response.content, status=response.status_code,
                                headers=response.headers)
        else:
            return HttpResponse(response.streaming_content,
                                status=response.status_code,
                                headers=response.headers)

    def _process_headers(self, request):
        # Copy headers that must be forwarded
        headers = {
            k: v for k, v in HttpHeaders(request.META).items()
            if k in self.proxy_settings.FORWARD_HEADERS
        }
        return self.process_headers(request, headers)

    def _process_data(self, request):
        if request.content_type.startswith('multipart'):
            data = request.data
            if request.FILES:
                for file, _ in request.FILES.items():
                    data.pop(file, None)
        else:
            data = request.body
        return self.process_data(request, data)

    def _process_files(self, request):
        if request.content_type.startswith('multipart') and request.FILES:
            files = {k: v for k, v in request.FILES.items()}
            return self.process_files(request, files)
        return None

    def process_headers(self, request, headers: dict) -> dict:
        return headers

    def process_data(self, request, data):
        return data

    def process_files(self, request, files: dict) -> dict:
        return files

    def process_response(self, response):
        return response
