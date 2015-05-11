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

    @classmethod
    def create(cls):
        session = cls()
        DBSession.add(session)
        DBSession.flush()
        return session
