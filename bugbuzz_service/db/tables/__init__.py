from __future__ import unicode_literals
import datetime

import pytz
from sqlalchemy import MetaData
from sqlalchemy.sql.expression import func


metadata = MetaData()


#: The now function for database relative operation
_now_func = [func.utc_timestamp]


def set_now_func(func):
    """Replace now function and return the old function
   
    """
    old = _now_func[0]
    _now_func[0] = func
    return old


def get_now_func():
    """Return current now func
   
    """
    return _now_func[0]


def now_func():
    """Return current datetime
   
    """
    func = get_now_func()
    dt = func()
    if isinstance(dt, datetime.datetime):
        if dt.tzinfo is None:
            return dt.replace(tzinfo=pytz.utc)
    return dt

from .debug_sessions import debug_sessions  # noqa
