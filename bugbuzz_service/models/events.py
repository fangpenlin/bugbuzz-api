from __future__ import unicode_literals

from ..db import tables
from ..db import DBSession
from .base import Base


class Event(Base):
    __table__ = tables.events

    @classmethod
    def create(cls, session, type, params=None):
        event = cls(session=session, type=type, params=params)
        DBSession.add(event)
        DBSession.flush()
        return event
