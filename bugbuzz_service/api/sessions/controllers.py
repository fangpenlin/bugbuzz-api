from __future__ import unicode_literals

from pyramid.httpexceptions import HTTPBadRequest
from pyramid.settings import asbool
from pyramid.view import view_config

from ... import models
from ...db import db_transaction
from ...renderers import event_adapter
from ..base import ControllerBase
from ..base import view_defaults
from .resources import SessionActionResource
from .resources import SessionIndexResource
from .resources import SessionResource


@view_defaults(context=SessionIndexResource)
class SessionIndexController(ControllerBase):

    @view_config(request_method='POST')
    def post(self):
        encrypted = asbool(self.request.params.get('encrypted', False))
        kwargs = {}
        if encrypted:
            if (
                'aes_iv' not in self.request.params or
                'validation_code' not in self.request.params or
                'encrypted_code' not in self.request.params
            ):
                return HTTPBadRequest(
                    'Need to provide aes_iv, validation_code and '
                    'encrypted_code for encrypted session'
                )
            kwargs['aes_iv'] = self.request.params['aes_iv'].file.read()
            kwargs['validation_code'] = self.request.params['validation_code']
            kwargs['encrypted_code'] = (
                self.request.params['encrypted_code'].file.read()
            )
        with db_transaction():
            session = models.Session.create(
                encrypted=encrypted,
                **kwargs
            )
        self.request.response.status = '201 Created'
        return dict(session=session)


@view_defaults(context=SessionResource)
class SessionController(ControllerBase):

    @view_config(request_method='GET')
    def get(self):
        return dict(session=self.context.entity)


@view_defaults(context=SessionActionResource)
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
        self.publish_event(
            self.context.entity.client_channel_id,
            {'event': event_adapter(event, self.request)},
        )
        return event

    @view_config(name='return', request_method='POST')
    def return_post(self):
        return self._command_post('return')

    @view_config(name='next', request_method='POST')
    def next_post(self):
        return self._command_post('next')

    @view_config(name='step', request_method='POST')
    def step_post(self):
        return self._command_post('step')

    @view_config(name='continue', request_method='POST')
    def continue_post(self):
        return self._command_post('continue')
