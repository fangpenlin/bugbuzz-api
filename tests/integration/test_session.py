import base64

import pytest
from webtest import Upload


def test_create_session(testapp):
    resp = testapp.post('/sessions', status=201)
    assert resp.json['session']['id'].startswith('SE')


def test_create_encrypted_session(testapp):
    validation_code = 'suuper_foobar'
    resp = testapp.post(
        '/sessions',
        dict(
            encrypted='true',
            validation_code=validation_code,
            encrypted_code=Upload('encrypted_code', b'encrypted'),
            aes_iv=Upload('aes_iv', b'0123456789ABCDEF'),
        ),
        status=201,
    )
    assert resp.json['session']['id'].startswith('SE')
    assert resp.json['session']['encrypted']
    assert (
        base64.b64decode(resp.json['session']['aes_iv']) == b'0123456789ABCDEF'
    )
    assert resp.json['session']['validation_code'] == validation_code


@pytest.mark.parametrize('params', [
    dict(
        encrypted='true',
    ),
    dict(
        encrypted='true',
        validation_code='suuper_foobar',
        encrypted_code=Upload('encrypted_code', b'encrypted'),
    ),
    dict(
        encrypted='true',
        encrypted_code=Upload('encrypted_code', b'encrypted'),
        aes_iv=Upload('aes_iv', b'0123456789ABCDEF'),
    ),
    dict(
        encrypted='true',
        validation_code='suuper_foobar',
        aes_iv=Upload('aes_iv', b'0123456789ABCDEF'),
    ),
])
def test_create_encrypted_session_with_bad_params(testapp, params):
    testapp.post(
        '/sessions',
        params,
        status=400,
    )


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
