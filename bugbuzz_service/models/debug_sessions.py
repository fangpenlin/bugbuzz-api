from __future__ import unicode_literals

from ..db import tables
from ..db import Session
from .base import Base


class DebugSession(Base):
    __table__ = tables.debug_sessions

    @classmethod
    def create(cls):
        debug_session = cls()
        Session.add(debug_session)
        Session.flush()
        return debug_session
