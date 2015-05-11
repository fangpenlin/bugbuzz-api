from __future__ import unicode_literals

from pyramid.view import view_config

from ... import models
from ...db import db_transaction
from ...renderers import file_adapter
from ..base import ControllerBase
from ..base import view_defaults
from .resources import FileIndexResource


@view_defaults(context=FileIndexResource)
class FileIndexController(ControllerBase):

    @view_config(request_method='POST')
    def post(self):
        # settings = self.request.registry.settings
        with db_transaction():
            file_ = models.File.create(
                session=self.context.entity,
                filename=self.request.params['file'].filename,
                mime_type=self.request.params['file'].type,
                content=self.request.params['file'].file.read(),
            )
        self.publish_event(
            file_.session.guid,
            dict(file=file_adapter(file_, self.request)),
        )
        self.request.response.status = '201 Created'
        return file_
