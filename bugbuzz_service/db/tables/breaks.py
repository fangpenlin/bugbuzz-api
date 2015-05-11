from __future__ import unicode_literals

from sqlalchemy import Column
from sqlalchemy import Unicode
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy.schema import ForeignKey

from ...utils import GUIDFactory
from .utc_dt import UTCDateTime
from . import metadata
from . import now_func


breaks = Table(
    'breaks',
    metadata,
    Column('guid', Unicode(64), primary_key=True, default=GUIDFactory('BK')),
    Column('session_guid', Unicode(64), ForeignKey(
        'sessions.guid',
        ondelete='CASCADE',
        onupdate='CASCADE',
    ), nullable=False, index=True),
    # filename for current break
    Column('filename', Unicode, nullable=False),
    # lineno for current break
    Column('lineno', Integer, nullable=False),
    # TODO: call stack (frames)
    # TODO: variables
    Column('created_at', UTCDateTime, default=now_func),
    Column(
        'updated_at',
        UTCDateTime,
        default=now_func,
        onupdate=now_func,
    ),
)
