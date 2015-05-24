from __future__ import unicode_literals

from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import view_config

from ... import models
from ...db import db_transaction
from ...renderers import break_adapter
from ..base import ControllerBase
from ..base import view_defaults
from .resources import BreakIndexResource
from .resources import BreakResource


@view_defaults(context=BreakIndexResource)
class BreakIndexController(ControllerBase):

    @view_config(request_method='POST')
    def post(self):
        with db_transaction():
            aes_iv = None
            if 'aes_iv' in self.request.params:
                aes_iv = self.request.params['aes_iv'].file.read()
            if self.context.entity.encrypted and aes_iv is None:
                return HTTPBadRequest(
                    'Need to provide aes_iv for encrypted session'
                )
            file_ = models.File.query.get(self.request.params['file_id'])
            break_ = models.Break.create(
                session=self.context.entity,
                file_=file_,
                lineno=self.request.params['lineno'],
                local_vars=self.request.params['local_vars'].file.read(),
                aes_iv=aes_iv,
            )
        self.publish_event(
            break_.session.dashboard_channel_id,
            {'break': break_adapter(break_, self.request)},
        )
        self.request.response.status = '201 Created'
        return {'break': break_}


@view_defaults(context=BreakResource)
class BreakController(ControllerBase):

    @view_config(request_method='GET')
    def get(self):
        return {'break': self.context.entity}
