from django.conf import settings as dj_settings
from misago.conf import settings as mi_settings

from . import defaults


class SettingsGateway(object):
    def __getattr__(self, name):
        try:
            return getattr(dj_settings, name)
        except AttributeError:
            pass

        try:
            return getattr(mi_settings, name)
        except AttributeError:
            pass

        return getattr(defaults, name)


settings = SettingsGateway()
