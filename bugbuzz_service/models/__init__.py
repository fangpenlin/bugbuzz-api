from __future__ import unicode_literals
import datetime

import pytz
from sqlalchemy import engine_from_config

from ..db import tables
from ..db import DBSession


def setup_database(global_config, **settings):
    """Setup database
   
    """
    if 'engine' not in settings:
        connect_args = {}
        if settings['sqlalchemy.url'].lower().startswith('postgres'):
            # We need to set timezone to UTC, as we use UTC for all our dt,
            # otherwise PostgreSQL will convert the given dt with local timezone
            connect_args['options'] = '-c timezone=utc'
        settings['engine'] = (
            engine_from_config(
                settings,
                'sqlalchemy.',
                connect_args=connect_args,
            )
        )
    DBSession.bind = settings['engine']
    tables.metadata.bind = settings['engine']

    def now_func():
        now = datetime.datetime.utcnow()
        return now.replace(tzinfo=pytz.utc)

    tables.set_now_func(now_func)
    return settings

from .sessions import Session  # noqa
from .events import Event  # noqa
from .breaks import Break  # noqa
from .files import File  # noqa
