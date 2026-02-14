from rest_framework.views import APIView
from rest_framework import permissions
from apps.rest_api_proxy.settings import rest_api_proxy_settings
import requests


class ProxyBase(APIView):
    proxy_settings = rest_api_proxy_settings

    def proxy_host(self):
        return self.proxy_settings.HOST

    def proxy_url(self, request):
        return ''.join([self.proxy_host(), request.get_full_path()])

    def forward(self, request):
        return requests.request(request.method, self.proxy_url(request))

    def get(self, request, format=None):
        new_request = self.process_request(request)
        new_response = self.process_response(self.forward(new_request))
        return new_response

    def process_request(self, request):
        return request

    def process_response(self, response):
        return response
