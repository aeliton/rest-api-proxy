from rest_framework.views import APIView
from rest_api_proxy.settings import rest_api_proxy_settings, RAPSettings
from django.http import HttpHeaders, HttpResponse
import requests


class ProxyBase(APIView):
    """
    Basic proxy class to enable simple interceptor implementation.

    Default Behaviour
    -----------------

    The default processing of the incoming request is to construct a new request
    from parts of the incoming request. The members of the request that are
    forwarded and how they are processed by default are:

    files: are extracted to be sent to the target as they come. Override
    `process_files` to change this behaviour.

    data: case `data` is of type dict, all file entries (from request.FILES)
    will be removed to avoid duplication. Override `process_data` to change this
    behaviour.

    headers: Only HTTP headers (e.g. 'Authorization') explicitly set in
    `FORWARD_HEADERS` settings will be forwarded. Override `process_headers` to
    change this behaviour.

    Once the new request is constructed as described above, it will be sent to
    the target API and the response received will be then passed through
    `process_response` that can construct a modified response object to be
    returned to the request originator.

    Attributes:
        proxy_settings: Settings to be used to initialize the instance.
    """
    proxy_settings: dict = None

    def __init__(self, proxy_settings=None):
        """
        Initializes a ProxyBase instance.

        Arguments:
        ----------

        proxy_settings: dict containing the following entries and values:
        - HOST: str, the target server URL.
        - FORWARD_HEADERS: list[str], all headers from the incoming request
          that must be forwarded to the target server (e.g. 'Authorization').
        """
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
        """
        Processes the incoming request headers.

        Override this function to return the desired set of headers to be sent
        to the target API.

        Arguments
        ---------
        request: the incoming request.
        headers: dict, headers defined in `FORWARD_HEADERS` and their respective
        values extracted from `request`.

        Returns
        -------
        dict containing the HTTP headers and their values.
        """
        return headers

    def process_data(self, request, data):
        """
        Process the incoming request data.

        Override this function to alter the request.data.

        Arguments
        ---------
        request: the incoming request.
        data: dict or text, extracted from request.data.

        Returns
        -------
        dict or text to be set as request.data to be sent to the target API.
        """
        return data

    def process_files(self, request, files: dict) -> dict:
        """
        Process the incoming request files.

        Override this function to alter the files received in the incoming
        request.

        Arguments
        ---------
        request: the incoming request.
        files: dict of str and file-like objects, extracted from
        request.FILES.

        Returns
        -------
        dict containing {'file names': <file-like-object>}.
        """
        return files

    def process_response(self, response):
        """
        Process the outgoing request.

        Override this function to alter the response given by the target API.

        Arguments
        ---------
        response: the response received from the target API.

        Returns
        -------
        a response object to be sent as reply for the incoming request.
        """
        return response
