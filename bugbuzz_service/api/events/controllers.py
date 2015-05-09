from __future__ import unicode_literals

from pyramid.view import view_config
from pyramid.view import view_defaults

from ... import models
from ..base import ControllerBase
from .resources import EventIndexResource


@view_defaults(
    context=EventIndexResource,
    renderer='json',
)
class EventIndexController(ControllerBase):

    @view_config(request_method='GET')
    def get(self):
        # TODO: pagination and filtering by last event ID
        return dict(
            events=models.Event.query.all(),
        )
