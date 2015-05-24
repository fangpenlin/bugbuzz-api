from __future__ import unicode_literals

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import Unicode

from . import metadata
from . import now_func
from ...utils import GUIDFactory
from .utc_dt import UTCDateTime


sessions = Table(
    'sessions',
    metadata,
    Column('guid', Unicode(64), primary_key=True, default=GUIDFactory('SE')),
    Column('encrypted', Boolean, nullable=False, default=False),
    Column('created_at', UTCDateTime, default=now_func),
    Column(
        'updated_at',
        UTCDateTime,
        default=now_func,
        onupdate=now_func,
    ),
)
