from __future__ import unicode_literals
import contextlib

import transaction
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from zope.sqlalchemy import ZopeTransactionExtension


Session = scoped_session(sessionmaker(
    extension=ZopeTransactionExtension(keep_session=True),
))


@contextlib.contextmanager
def db_transaction():
    with transaction.manager:
        yield
        Session.flush()
