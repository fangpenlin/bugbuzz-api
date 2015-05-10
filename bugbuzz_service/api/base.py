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


view_defaults = functools.partial(view.view_defaults, renderer='json')
