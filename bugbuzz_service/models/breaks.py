from __future__ import unicode_literals

from ..db import DBSession
from ..db import tables
from .base import Base


class Break(Base):
    __table__ = tables.breaks

    @classmethod
    def create(cls, session, file_, lineno, local_vars, aes_iv=None):
        break_ = cls(
            session=session,
            file=file_,
            lineno=lineno,
            local_vars=local_vars,
            aes_iv=aes_iv,
        )
        DBSession.add(break_)
        DBSession.flush()
        return break_
