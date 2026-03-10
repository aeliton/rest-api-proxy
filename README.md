![unit-tests][1] ![e2e-tests][2]

# rest-api-proxy

Another [DRF](https://www.django-rest-framework.org/) API proxy to redirect
incoming requests to another API server, but with the option of altering the
request and the response.

The original use case that motivated this implementation is to have a node
responsible for the encryption/decryption of payloads, so that cryptographic
keys are kept separated from the data.

## TODO

* Add options to inject extra headers
* Add extra options to inject authentication data
* Add examples that alters requests

# Usage

## Setting the target server

The target server can be defined in *settings.py* by setting the `HOST` URL
entry in the `REST_API_PROXY` dictionary as follows:

```python
# settings.py
REST_API_PROXY = {
    'HOST': 'http://real-handler.com',
}
```

This can be set also directly to the instance via:

```python
proxy = ProxyBase.as_view(proxy_settings={'HOST': 'http://real-handler.com'})
```

## Request altering

Altering the request is achieved by extending the `ProxyBase` class.

```python
class Proxy(ProxyBase):
    def process_request(self, request):
        # alter you request here
        return request

    def process_response(self, response):
        # alter you response here
        return response
```

## Development

To install dependencies run:

```bash
uv sync --dev
```

## Running tests

```bash
python runtests.py
```

# License

[rest-api-proxy](README.md) is offered under the BSD-2-Clause license.

# Credits

This work is inspired by
[django-api-proxy](https://github.com/aiselis/django-api-proxy/) (Simplified BSD
License).

[1]: https://github.com/aeliton/rest-api-proxy/actions/workflows/python-app.yml/badge.svg?branch=main 
[2]: https://github.com/aeliton/rest-api-proxy/actions/workflows/e2e-tests.yml/badge.svg?branch=main
