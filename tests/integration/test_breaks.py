import base64
import json

from webtest import Upload


def test_create_break(testapp, session):
    sid = session['id']

    resp = testapp.post(
        '/sessions/{}/files'.format(sid),
        dict(
            file=Upload('foobar.py', b'print 123'),
        ),
        status=201,
    )
    file_id = resp.json['file']['id']

    resp = testapp.post(
        '/sessions/{}/breaks'.format(sid),
        dict(
            lineno='123',
            file_id=file_id,
            local_vars=Upload('local_vars', json.dumps(dict(
                foo='bar',
                eggs='spam',
            )).encode('utf8')),
        ),
        status=201,
    )
    assert resp.json['break']['id'].startswith('BK')
    assert resp.json['break']['file'] == file_id
    assert resp.json['break']['lineno'] == 123
    local_vars = json.loads(base64.b64decode(resp.json['break']['local_vars']))
    assert local_vars == dict(
        foo='bar',
        eggs='spam',
    )


def test_create_encrypted_break_without_iv(testapp, encrypted_session):
    sid = encrypted_session['id']
    resp = testapp.post(
        '/sessions/{}/files'.format(sid),
        dict(
            file=Upload('foobar.py', b'print 123'),
            aes_iv=Upload('aes_iv', b'0123456789ABCDEF'),
        ),
        status=201,
    )
    file_id = resp.json['file']['id']
    testapp.post(
        '/sessions/{}/breaks'.format(sid),
        dict(
            lineno='123',
            file_id=file_id,
            local_vars=Upload('local_vars', json.dumps(dict(
                foo='bar',
                eggs='spam',
            )).encode('utf8')),
        ),
        status=400,
    )


def test_create_encrypted_break(testapp, encrypted_session):
    sid = encrypted_session['id']
    resp = testapp.post(
        '/sessions/{}/files'.format(sid),
        dict(
            file=Upload('foobar.py', b'print 123'),
            aes_iv=Upload('aes_iv', b'0123456789ABCDEF'),
        ),
        status=201,
    )
    file_id = resp.json['file']['id']
    resp = testapp.post(
        '/sessions/{}/breaks'.format(sid),
        dict(
            lineno='123',
            file_id=file_id,
            local_vars=Upload('local_vars', json.dumps(dict(
                foo='bar',
                eggs='spam',
            )).encode('utf8')),
            aes_iv=Upload('aes_iv', b'0123456789ABCDEF'),
        ),
        status=201,
    )
    assert base64.b64decode(resp.json['break']['aes_iv']) == b'0123456789ABCDEF'


def test_get_break(testapp, session):
    sid = session['id']

    resp = testapp.post(
        '/sessions/{}/files'.format(sid),
        dict(
            file=Upload('foobar.py', b'print 123'),
        ),
        status=201,
    )
    file_id = resp.json['file']['id']

    resp = testapp.post(
        '/sessions/{}/breaks'.format(sid),
        dict(
            lineno='123',
            file_id=file_id,
            local_vars=Upload('local_vars', json.dumps(dict(
                foo='bar',
                eggs='spam',
            )).encode('utf8')),
        ),
        status=201,
    )
    break_ = resp.json['break']

    resp = testapp.get('/breaks/{}'.format(break_['id']))
    assert resp.json['break'] == break_
