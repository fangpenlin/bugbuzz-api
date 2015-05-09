from __future__ import unicode_literals

import dateutil.parser
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
        query = models.Event.query.order_by(models.Event.created_at.asc())
        events = []
        last_timestamp = self.request.params.get('last_timestamp')
        if last_timestamp is not None:
            # Notice: the timestamp we use must be accurate, otherwise,
            # it's possible we will miss some event
            last_timestamp = dateutil.parser.parse(last_timestamp)
            query = query.filter(models.Event.created_at > last_timestamp)
        events = query.all()
        return dict(events=events)
