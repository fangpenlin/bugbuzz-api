from __future__ import unicode_literals

from ..db import tables
from ..db import DBSession
from .base import Base


class Break(Base):
    __table__ = tables.breaks

    @classmethod
    def create(cls, session, filename, lineno):
        break_ = cls(session=session, filename=filename, lineno=lineno)
        DBSession.add(break_)
        DBSession.flush()
        return break_
