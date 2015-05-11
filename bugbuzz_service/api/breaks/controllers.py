from __future__ import unicode_literals

from pyramid.view import view_config

from ... import models
from ...db import db_transaction
from ..base import ControllerBase
from ..base import view_defaults
from .resources import BreakIndexResource


@view_defaults(context=BreakIndexResource)
class BreakIndexController(ControllerBase):

    @view_config(request_method='POST')
    def post(self):
        with db_transaction():
            break_ = models.Break.create(
                session=self.context.entity,
                filename=self.request.params['filename'],
                lineno=self.request.params['lineno'],
            )
        self.request.response.status = '201 Created'
        return break_