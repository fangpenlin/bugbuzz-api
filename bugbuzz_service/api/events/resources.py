from __future__ import unicode_literals

from ... import models
from ..base import ResourceBase


class EventIndexResource(ResourceBase):

    def __getitem__(self, key):
        event = models.Event.query.get(key)
        if event is None:
            return
        return EventResource(
            self.request,
            parent=self,
            name=key,
            entity=event,
        )


class EventResource(ResourceBase):
    pass
