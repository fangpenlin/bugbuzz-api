from __future__ import unicode_literals

from ..db import tables
from ..db import DBSession
from .base import Base


class Break(Base):
    __table__ = tables.breaks

    @classmethod
    def create(cls, session, file_, lineno, local_vars):
        break_ = cls(
            session=session,
            file=file_,
            lineno=lineno,
            local_vars=local_vars,
        )
        DBSession.add(break_)
        DBSession.flush()
        return break_
