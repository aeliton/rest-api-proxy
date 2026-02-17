from rest_framework.views import APIView
from apps.rest_api_proxy.settings import rest_api_proxy_settings, RAPSettings
import requests


class ProxyBase(APIView):
    def __init__(self, proxy_settings=None):
        super().__init__()

        if proxy_settings:
            self.proxy_settings = RAPSettings(proxy_settings)
        else:
            self.proxy_settings = rest_api_proxy_settings

        for method in self.http_method_names:
            setattr(self, method, self.forward)

    def proxy_host(self):
        return self.proxy_settings.HOST

    def proxy_url(self, request):
        return ''.join([self.proxy_host(), request.get_full_path()])

    def forward(self, incoming_request):
        request = self.process_request(incoming_request)
        response = requests.request(request.method, self.proxy_url(request))
        return self.process_response(response)

    def process_request(self, request):
        return request

    def process_response(self, response):
        return response
