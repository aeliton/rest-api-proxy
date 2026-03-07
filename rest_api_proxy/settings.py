from django.conf import settings

DEFAULTS = {
    'HOST': None,
    'FORWARD_HEADERS': []
}


class RAPSettings:
    def __init__(self, overrides=None):
        self._overrides = overrides
        self.defaults = DEFAULTS

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid REST_API_PROXY setting: '%s'" % attr)

        try:
            val = self._overrides[attr]
        except KeyError:
            val = self.defaults[attr]

        setattr(self, attr, val)
        return val


REST_API_PROXY = getattr(settings, 'REST_API_PROXY', None)
rest_api_proxy_settings = RAPSettings(overrides=REST_API_PROXY)
