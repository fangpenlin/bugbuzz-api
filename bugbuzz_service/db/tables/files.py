from __future__ import unicode_literals

from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import Unicode
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.schema import ForeignKey

from . import metadata
from . import now_func
from ...utils import GUIDFactory
from .utc_dt import UTCDateTime


files = Table(
    'files',
    metadata,
    Column('guid', Unicode(64), primary_key=True, default=GUIDFactory('FL')),
    Column('session_guid', Unicode(64), ForeignKey(
        'sessions.guid',
        ondelete='CASCADE',
        onupdate='CASCADE',
    ), nullable=False, index=True),
    # name of file
    Column('filename', Unicode, nullable=False),
    # mime type of file
    Column('mime_type', Unicode, nullable=False),
    # TODO: save in amazon S3 instead?
    # file content
    Column('content', BYTEA, nullable=False),
    # AES 256 encryption IV
    Column('aes_iv', BYTEA),
    # TODO: add a hash column for querying files?
    Column('created_at', UTCDateTime, default=now_func),
    Column(
        'updated_at',
        UTCDateTime,
        default=now_func,
        onupdate=now_func,
    ),
)
