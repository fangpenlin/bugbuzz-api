from __future__ import unicode_literals

from pyramid.view import view_config
from pyramid.view import view_defaults

from ... import models
from ...db import db_transaction
from ..base import ControllerBase
from .resources import SessionIndexResource
from .resources import SessionActionResource


@view_defaults(
    context=SessionIndexResource,
    renderer='json',
)
class SessionIndexController(ControllerBase):

    @view_config(request_method='POST')
    def post(self):
        with db_transaction():
            session = models.Session.create()
        return session


@view_defaults(
    context=SessionActionResource,
    renderer='json',
)
class SessionActionController(ControllerBase):

    @view_config(name='next', request_method='POST')
    def next_post(self):
        with db_transaction():
            event = models.Event.create(
                session=self.context.entity,
                type='next',
            )
        return event
