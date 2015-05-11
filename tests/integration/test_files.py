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
