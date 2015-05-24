from __future__ import unicode_literals

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy import Unicode
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.schema import ForeignKey

from . import metadata
from . import now_func
from ...utils import GUIDFactory
from .utc_dt import UTCDateTime


breaks = Table(
    'breaks',
    metadata,
    Column('guid', Unicode(64), primary_key=True, default=GUIDFactory('BK')),
    Column('session_guid', Unicode(64), ForeignKey(
        'sessions.guid',
        ondelete='CASCADE',
        onupdate='CASCADE',
    ), nullable=False, index=True),
    Column('file_guid', Unicode(64), ForeignKey(
        'files.guid',
        ondelete='CASCADE',
        onupdate='CASCADE',
    ), nullable=False, index=True),
    # lineno for current break
    Column('lineno', Integer, nullable=False),
    Column('local_vars', BYTEA, nullable=False),
    # AES 256 encryption IV
    Column('aes_iv', BYTEA),
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
