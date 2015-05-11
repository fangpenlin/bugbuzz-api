from __future__ import unicode_literals

from ..db import tables
from ..db import DBSession
from .base import Base


class File(Base):
    __table__ = tables.files

    @classmethod
    def create(cls, session, filename, mime_type, content):
        file_ = cls(
            session=session,
            filename=filename,
            mime_type=mime_type,
            content=content,
        )
        DBSession.add(file_)
        DBSession.flush()
        return file_
