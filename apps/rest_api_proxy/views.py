from rest_framework.views import APIView
from rest_framework.response import Response
from apps.rest_api_proxy.settings import rest_api_proxy_settings, RAPSettings
import requests


class ProxyBase(APIView):
    proxy_settings = None

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

    def proxy(self, request):
        input = self.process_request(request)
        output = self.process_response(
            requests.request(input.method, self.proxy_url(input))
        )
        return Response(status=output.status_code)

    def process_request(self, request):
        return request

    def process_response(self, response):
        return response
