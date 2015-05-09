from __future__ import unicode_literals

from pyramid.view import view_config
from pyramid.view import view_defaults

from ... import models
from ...db import db_transaction
from ..base import ControllerBase
from .resources import DebugSessionIndexResource


@view_defaults(
    context=DebugSessionIndexResource,
    renderer='json',
)
class DebugSessionIndexController(ControllerBase):

    @view_config(request_method='POST')
    def post(self):
        with db_transaction():
            debug_session = models.DebugSession.create()
        return debug_session
