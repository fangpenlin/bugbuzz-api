from __future__ import unicode_literals

import os

import pytest
from webtest import TestApp

from bugbuzz_service import main
from bugbuzz_service import models
from bugbuzz_service.db import DBSession
from bugbuzz_service.db.tables import metadata


@pytest.yield_fixture
def database(settings=None):
    settings = settings or {}
    app_settings = settings.copy()
    db_url = os.environ.get(
        'TEST_DB',
        'postgres://bugbuzz:bugbuzz@127.0.0.1/bugbuzz_test',
    )
    app_settings['sqlalchemy.url'] = db_url
    app_settings = models.setup_database({}, **app_settings)
    metadata.bind = app_settings['engine']
    metadata.create_all()
    yield app_settings
    DBSession.close()
    DBSession.remove()
    metadata.drop_all()


@pytest.fixture
def testapp(database, settings=None):
    app_settings = settings or {
        'db_session_cleanup': False,
        'pubnub.publish_key': 'DUMMY_PUB_KEY',
        'pubnub.subscribe_key': 'DUMMY_SUB_KEY',
    }
    app_settings.update(database)
    app = main({}, **app_settings)
    testapp = TestApp(app)
    return testapp


@pytest.fixture
def session(testapp):
    resp = testapp.post(
        '/sessions',
    )
    return resp.json['session']


@pytest.fixture
def session2(testapp):
    resp = testapp.post(
        '/sessions',
    )
    return resp.json['session']


@pytest.fixture
def encrypted_session(testapp):
    resp = testapp.post_json(
        '/sessions',
        dict(encrypted=True),
    )
    return resp.json['session']
