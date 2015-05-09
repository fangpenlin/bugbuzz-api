from __future__ import unicode_literals

from ..db import tables
from ..db import DBSession
from .base import Base


class Event(Base):
    __table__ = tables.events

    @classmethod
    def create(cls, session, type, parameters=None):
        event = cls(session=session, type=type, parameters=parameters)
        DBSession.add(event)
        DBSession.flush()
        return event
