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

    def _command_post(self, command):
        with db_transaction():
            event = models.Event.create(
                session=self.context.entity,
                type=command,
                params=(
                    dict(self.request.POST)
                    if self.request.POST is not None else None
                ),
            )
        return event

    @view_config(name='next', request_method='POST')
    def next_post(self):
        return self._command_post('next')

    @view_config(name='step', request_method='POST')
    def step_post(self):
        return self._command_post('step')

    @view_config(name='continue', request_method='POST')
    def continue_post(self):
        return self._command_post('continue')
