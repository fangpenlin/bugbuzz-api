from __future__ import unicode_literals

from ... import models
from ..base import ResourceBase


class BreakIndexResource(ResourceBase):

    def __getitem__(self, key):
        break_ = models.Break.query.get(key)
        if break_ is None:
            return
        return BreakResource(
            self.request,
            parent=self,
            name=key,
            entity=break_,
        )


class BreakResource(ResourceBase):
    pass
