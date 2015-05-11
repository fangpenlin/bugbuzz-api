from __future__ import unicode_literals

from ... import models
from ..base import ResourceBase


class FileIndexResource(ResourceBase):

    def __getitem__(self, key):
        file_ = models.File.query.get(key)
        if file_ is None:
            return
        return FileResource(
            self.request,
            parent=self,
            name=key,
            entity=file_,
        )


class FileResource(ResourceBase):
    pass
