from __future__ import unicode_literals

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
            file_ = models.File.query.get(self.request.params['file_id'])
            break_ = models.Break.create(
                session=self.context.entity,
                file_=file_,
                lineno=self.request.params['lineno'],
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
