from __future__ import unicode_literals

from sqlalchemy import Column
from sqlalchemy import Unicode
from sqlalchemy import Table

from ...utils import GUIDFactory
from .utc_dt import UTCDateTime
from . import metadata
from . import now_func


sessions = Table(
    'sessions',
    metadata,
    Column('guid', Unicode(64), primary_key=True, default=GUIDFactory('SE')),
    Column('created_at', UTCDateTime, default=now_func),
    Column(
        'updated_at',
        UTCDateTime,
        default=now_func,
        onupdate=now_func,
    ),
)
