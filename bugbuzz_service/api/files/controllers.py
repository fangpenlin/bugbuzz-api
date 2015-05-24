from __future__ import unicode_literals

from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import view_config

from ... import models
from ...db import db_transaction
from ...renderers import file_adapter
from ..base import ControllerBase
from ..base import view_defaults
from .resources import FileIndexResource
from .resources import FileResource


@view_defaults(context=FileIndexResource)
class FileIndexController(ControllerBase):

    @view_config(request_method='POST')
    def post(self):
        # settings = self.request.registry.settings
        with db_transaction():
            aes_iv = None
            if 'aes_iv' in self.request.params:
                aes_iv = self.request.params['aes_iv'].file.read()
            if self.context.entity.encrypted and aes_iv is None:
                return HTTPBadRequest(
                    'Need to provide aes_iv for encrypted session'
                )

            file_ = models.File.create(
                session=self.context.entity,
                filename=self.request.params['file'].filename,
                mime_type=self.request.params['file'].type,
                content=self.request.params['file'].file.read(),
                aes_iv=aes_iv,
            )
        self.publish_event(
            file_.session.guid,
            dict(file=file_adapter(file_, self.request)),
        )
        self.request.response.status = '201 Created'
        return dict(file=file_)


@view_defaults(context=FileResource)
class FileController(ControllerBase):

    @view_config(request_method='GET')
    def get(self):
        return dict(file=self.context.entity)
