from __future__ import unicode_literals

from sqlalchemy import Column
from sqlalchemy import Unicode
from sqlalchemy import UnicodeText
from sqlalchemy import Table
from sqlalchemy.schema import ForeignKey

from ...utils import GUIDFactory
from .utc_dt import UTCDateTime
from . import metadata
from . import now_func


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
    Column('content', UnicodeText, nullable=False),
    # TODO: add a hash column for querying files?
    Column('created_at', UTCDateTime, default=now_func),
    Column(
        'updated_at',
        UTCDateTime,
        default=now_func,
        onupdate=now_func,
    ),
)
