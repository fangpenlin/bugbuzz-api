from __future__ import unicode_literals

from pyramid.renderers import JSON
from pyramid.settings import asbool

from . import models


def session_adapter(session, request):
    return dict(
        id=session.guid,
        created_at=session.created_at.isoformat(),
        updated_at=session.created_at.isoformat(),
    )


def event_adapter(event, request):
    return dict(
        id=event.guid,
        type=event.type,
        params=event.params,
        created_at=event.created_at.isoformat(),
        updated_at=event.created_at.isoformat(),
    )


def enum_symbol(enum_value):
    if enum_value is None:
        return enum_value
    return str(enum_value).lower()


def includeme(config):
    settings = config.registry.settings
    kwargs = {}
    cfg_key = 'api.json.pretty_print'
    pretty_print = asbool(settings.get(cfg_key, True))
    if pretty_print:
        kwargs = dict(sort_keys=True, indent=4, separators=(',', ': '))

    json_renderer = JSON(**kwargs)
    json_renderer.add_adapter(models.Session, session_adapter)
    json_renderer.add_adapter(models.Event, event_adapter)
    config.add_renderer('json', json_renderer)
