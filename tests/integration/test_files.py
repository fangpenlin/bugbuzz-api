from __future__ import unicode_literals

from webtest import Upload


def test_create_file(testapp, session):
    sid = session['id']
    resp = testapp.post(
        '/sessions/{}/files'.format(sid),
        dict(
            file=Upload('foobar.py', b'print 123'),
        ),
        status=201,
    )
    assert resp.json['file']['id'].startswith('FL')
    assert resp.json['file']['filename'] == 'foobar.py'
    assert resp.json['file']['content'].decode('base64') == 'print 123'


def test_create_encrypted_file_without_iv(testapp, encrypted_session):
    sid = encrypted_session['id']
    testapp.post(
        '/sessions/{}/files'.format(sid),
        dict(
            file=Upload('foobar.py', b'print 123'),
        ),
        status=400,
    )


def test_create_encrypted_file(testapp, encrypted_session):
    sid = encrypted_session['id']
    resp = testapp.post(
        '/sessions/{}/files'.format(sid),
        dict(
            file=Upload('foobar.py', b'print 123'),
            aes_iv=Upload('aes_iv', b'0123456789ABCDEF'),
        ),
        status=201,
    )
    assert resp.json['file']['id'].startswith('FL')
    assert resp.json['file']['filename'] == 'foobar.py'
    assert resp.json['file']['content'].decode('base64') == b'print 123'
    assert resp.json['file']['aes_iv'].decode('base64') == b'0123456789ABCDEF'


def test_get_file(testapp, session):
    sid = session['id']
    resp = testapp.post(
        '/sessions/{}/files'.format(sid),
        dict(
            file=Upload('foobar.py', b'print 123'),
        ),
        status=201,
    )
    file_ = resp.json['file']

    resp = testapp.get('/files/{}'.format(file_['id']))
    assert resp.json['file'] == file_
