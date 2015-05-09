from __future__ import unicode_literals

from ... import models
from ..base import ResourceBase


class DebugSessionIndexResource(ResourceBase):

    def __getitem__(self, key):
        debug_session = models.DebugSession.query.get(key)
        if debug_session is None:
            return
        return DebugSessionResource(
            self.request,
            parent=self,
            name=key,
            entity=debug_session,
        )


class DebugSessionResource(ResourceBase):
    pass
