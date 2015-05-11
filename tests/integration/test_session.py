from __future__ import unicode_literals

import pytest


def test_create_session(testapp):
    resp = testapp.post('/sessions', status=201)
    assert resp.json['id'].startswith('SE')


def test_get_session(testapp, session):
    resp = testapp.get('/sessions/{}'.format(session['id']))
    assert resp.json == dict(session=session)


@pytest.mark.parametrize('command, params', [
    ('next', {}),
    ('step', {}),
    ('continue', {}),
])
def test_basic_commands(testapp, session, command, params):
    sid = session['id']
    resp = testapp.post('/sessions/{}/actions/{}'.format(sid, command), params)
    event = resp.json
    assert event['id'].startswith('EV')
    assert event['type'] == command
    assert event['params'] == params
    resp = testapp.get('/sessions/{}/events'.format(sid))
    assert len(resp.json['events']) == 1
    assert resp.json['events'][0] == event
