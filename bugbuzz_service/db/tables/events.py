from __future__ import unicode_literals

from sqlalchemy import Column
from sqlalchemy import Unicode
from sqlalchemy import Table
from sqlalchemy.schema import ForeignKey
from sqlalchemy.dialects.postgresql import JSON

from ...utils import GUIDFactory
from .utc_dt import UTCDateTime
from . import metadata
from . import now_func


events = Table(
    'events',
    metadata,
    Column('guid', Unicode(64), primary_key=True, default=GUIDFactory('EV')),
    Column('session_guid', Unicode(64), ForeignKey(
        'sessions.guid',
        ondelete='CASCADE',
        onupdate='CASCADE',
    ), nullable=False, index=True),
    # type of this event
    Column('type', Unicode, nullable=False),
    # parameters for this event
    Column('params', JSON),
    Column('created_at', UTCDateTime, default=now_func),
    Column(
        'updated_at',
        UTCDateTime,
        default=now_func,
        onupdate=now_func,
    ),
)
