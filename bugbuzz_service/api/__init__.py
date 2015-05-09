from __future__ import unicode_literals

from .sessions.resources import SessionIndexResource


class RootResource(object):
    __name__ = ''

    def __init__(self, request):
        self.request = request
        self.endpoint_map = {
            'sessions': SessionIndexResource,
        }

    def __getitem__(self, key):
        cls = self.endpoint_map.get(key)
        if cls is not None:
            return cls(self.request, parent=self, name=key)
        return None


def includeme(config):
    config.set_root_factory(RootResource)
