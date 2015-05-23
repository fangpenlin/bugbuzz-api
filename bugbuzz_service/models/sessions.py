from __future__ import unicode_literals

from sqlalchemy.orm import relationship

from ..db import tables
from ..db import DBSession
from .base import Base


class Session(Base):
    __table__ = tables.sessions

    events = relationship(
        'Event',
        lazy='dynamic',
        backref='session',
        cascade='all, delete-orphan',
        order_by='Event.created_at.asc()',
    )

    breaks = relationship(
        'Break',
        lazy='dynamic',
        backref='session',
        cascade='all, delete-orphan',
        order_by='Break.created_at.asc()',
    )

    files = relationship(
        'File',
        lazy='dynamic',
        backref='session',
        cascade='all, delete-orphan',
        order_by='File.created_at.asc()',
    )

    @classmethod
    def create(cls):
        session = cls()
        DBSession.add(session)
        DBSession.flush()
        return session

    @property
    def client_channel_id(self):
        """ID of event channel for debugging client

        """
        # TODO: use hash with secret here
        return 'client-{}'.format(self.guid)

    @property
    def dashboard_channel_id(self):
        """ID of event channel for dashboard

        """
        # TODO: use hash with secret here
        return 'dashboard-{}'.format(self.guid)
