from __future__ import unicode_literals
import os
env = os.environ

default_settings = {
    'api.version_header_value': 'bugbuzz_service:__version__',
    'api.revision_header_value': 'bugbuzz_service:__git_revision__',
    'sentry.dsn': env.get('SENTRY_DSN'),
    'pubnub.publish_key': env.get('PUBNUB_PUBLISH_KEY'),
    'pubnub.subscribe_key': env.get('PUBNUB_SUBSCRIBE_KEY'),
}
