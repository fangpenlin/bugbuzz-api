from __future__ import unicode_literals

from sqlalchemy.orm import relationship

from ..db import DBSession
from ..db import tables
from .base import Base


class File(Base):
    __table__ = tables.files

    breaks = relationship(
        'Break',
        lazy='dynamic',
        backref='file',
        cascade='all, delete-orphan',
        order_by='Break.created_at.asc()',
    )

    @classmethod
    def create(cls, session, filename, mime_type, content, aes_iv=None):
        file_ = cls(
            session=session,
            filename=filename,
            mime_type=mime_type,
            content=content,
            aes_iv=aes_iv,
        )
        DBSession.add(file_)
        DBSession.flush()
        return file_
