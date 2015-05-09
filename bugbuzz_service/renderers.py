from __future__ import unicode_literals

from pyramid.renderers import JSON
from pyramid.settings import asbool

from . import models


def debug_session_adapter(debug_session, request):
    return dict(
        id=debug_session.guid,
        created_at=debug_session.created_at.isoformat(),
        updated_at=debug_session.created_at.isoformat(),
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
    json_renderer.add_adapter(models.DebugSession, debug_session_adapter)
    config.add_renderer('json', json_renderer)
