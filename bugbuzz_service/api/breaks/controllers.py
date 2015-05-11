from __future__ import unicode_literals

from pyramid.view import view_config

from ... import models
from ...db import db_transaction
from ...renderers import break_adapter
from ..base import ControllerBase
from ..base import view_defaults
from .resources import BreakIndexResource


@view_defaults(context=BreakIndexResource)
class BreakIndexController(ControllerBase):

    @view_config(request_method='POST')
    def post(self):
        settings = self.request.registry.settings
        with db_transaction():
            break_ = models.Break.create(
                session=self.context.entity,
                filename=self.request.params['filename'],
                lineno=self.request.params['lineno'],
            )
        # XXX:
        import socket
        socket.TCP_KEEPINTVL = 0x101
        socket.TCP_KEEPCNT = 0x102
        from Pubnub import Pubnub
        # TODO: move to base controller?
        pubnub = Pubnub(
            publish_key=settings['pubnub.publish_key'],
            subscribe_key=settings['pubnub.subscribe_key'],
        )
        # TODO: move this to model?
        # TODO: publish to a hashed channel name?
        pubnub.publish(break_.session.guid, break_adapter(break_, self.request))
        self.request.response.status = '201 Created'
        return break_
