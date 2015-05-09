from __future__ import unicode_literals

import pytz
from sqlalchemy import types


class UTCDateTime(types.TypeDecorator):

    impl = types.DateTime

    def __init__(self, *args, **kwargs):
        if 'timezone' not in kwargs:
            kwargs['timezone'] = True
        super(UTCDateTime, self).__init__(*args, **kwargs)

    def process_bind_param(self, value, engine):
        if value is not None:
            return value.astimezone(pytz.utc)

    def process_result_value(self, value, engine):
        if value is not None:
            return value.replace(tzinfo=pytz.utc)
