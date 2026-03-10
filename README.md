![unit-tests][1] ![e2e-tests][2]

# rest-api-proxy

Another [DRF](https://www.django-rest-framework.org/) API proxy to redirect
incoming requests to another API server, but with the option of altering the
request and the response.

The original use case that motivated this implementation is to have a node
responsible for the encryption/decryption of payloads, so that cryptographic
keys are kept separated from the stored backend data. An example implementation
of this use case can be found in the `examples` folder.

## General functionality

`ProxyBase` is a view (inherits DRF's `APIView`) that allow altering incoming
requests `headers`, `data`, and `files` via inheritance. The base implementation
always creates a new request to be sent to the target API with the same `data`
and `files`. The `headers` are specially treated: only the headers explicitly
defined in the library configuration are forwarded to the target API.

The configuration can be made via `settings.py` or via the view constructor.

```python
# settings.py
REST_API_PROXY = {
    'HOST': 'http://api.target.com',
    'FORWARD_HEADERS': ['Authorization'] #  only Authorization will be forwarded
}

# via constructor
ProxyBase.as_view(proxy_settings={'HOST': '...', 'FORWARD_HEADERS': [...]})
```

To alter `headers`, `data` and `files`, you can do this:
```python
class AlterAll(ProxyBase):
    def process_headers(self, request, headers):
        return your_custom_headers

    def process_data(self, request, data):
        return your_custom_data

    def process_files(self, request, files):
        return your_custom_files
```

To alter the response received from the target API, you can implement
`process_response`.

```python
    def process_response(self, target_api_response):
        # your magic here
        return your_custom_response
```

Please refer to the examples folder for more practical details.

## TODO

* Add extra options to inject authentication data

## Development

To install dependencies run:

```bash
uv sync --dev
```

## Running tests

```bash
# unit tests
python runtests.py

# E2E tests
cd examples
docker compose build
docker compose up cipher -d
docker compose run tests-e2e sh test_cipher_e2e.sh
```

# License

[rest-api-proxy](README.md) is offered under the BSD-2-Clause license.

# Credits

This work is inspired by
[django-api-proxy](https://github.com/aiselis/django-api-proxy/) (Simplified BSD
License).

[1]: https://github.com/aeliton/rest-api-proxy/actions/workflows/python-app.yml/badge.svg?branch=main 
[2]: https://github.com/aeliton/rest-api-proxy/actions/workflows/e2e-tests.yml/badge.svg?branch=main
