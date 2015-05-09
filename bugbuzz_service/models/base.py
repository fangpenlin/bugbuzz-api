from __future__ import unicode_literals

from sqlalchemy.ext.declarative import declarative_base

from ..db import DBSession


class Model(object):
    def __repr__(self):
        columns = self.__mapper__.c.keys()
        class_name = self.__class__.__name__
        items = ', '.join([
            '%s=%s' % (col, repr(getattr(self, col))) for col in columns
        ])
        return '%s(%s)' % (class_name, items)


Base = declarative_base(cls=Model)
Base.query = DBSession.query_property()
