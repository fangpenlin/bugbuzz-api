from __future__ import unicode_literals
import functools

from pyramid import view


class ResourceBase(object):
    def __init__(self, request, parent=None, name=None, entity=None):
        self.__name__ = name
        self.__parent__ = parent
        self.request = request
        self.entity = entity


class ControllerBase(object):

    form_factory_cls = None

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.settings = self.request.registry.settings

    def publish_event(self, channel, event):
        # XXX: work around for missing attributes
        import socket
        socket.TCP_KEEPINTVL = 0x101
        socket.TCP_KEEPCNT = 0x102
        from Pubnub import Pubnub
        # TODO: move to base controller?
        pubnub = Pubnub(
            publish_key=self.settings['pubnub.publish_key'],
            subscribe_key=self.settings['pubnub.subscribe_key'],
        )
        return pubnub.publish(channel, event)


view_defaults = functools.partial(view.view_defaults, renderer='json')
