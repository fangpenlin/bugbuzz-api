from __future__ import unicode_literals

import pytest


@pytest.fixture
def session(testapp):
    resp = testapp.post(
        '/sessions',
    )
    return resp.json


def test_create_session(testapp):
    resp = testapp.post(
        '/sessions',
    )
    assert resp.json['id'].startswith('SE')


# TODO: parameterize for different commands
def test_next(testapp, session):
    sid = session['id']
    resp = testapp.post('/sessions/{}/actions/next'.format(sid))
    event = resp.json
    assert event['id'].startswith('EV')
    resp = testapp.get('/sessions/{}/events'.format(sid))
    assert len(resp.json['events']) == 1
    assert resp.json['events'][0] == event
