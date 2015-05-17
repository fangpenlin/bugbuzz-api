from __future__ import unicode_literals

from raven import Client
from raven.middleware import Sentry

import bugbuzz_service

# TODO: logging config?
application = bugbuzz_service.main({})

# configure sentry middleware if it's avaiable
if application.registry.settings.get('sentry.dsn'):
    application = Sentry(
        application,
        Client(application.registry.settings['sentry.dsn'])
    )
