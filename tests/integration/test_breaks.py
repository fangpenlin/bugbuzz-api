from __future__ import unicode_literals

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

    resp = testapp.post_json(
        '/sessions/{}/breaks'.format(sid),
        dict(
            lineno=123,
            file_id=file_id,
            local_vars=dict(
                foo='bar',
                eggs='spam',
            ),
        ),
        status=201,
    )
    assert resp.json['break']['id'].startswith('BK')
    assert resp.json['break']['file'] == file_id
    assert resp.json['break']['lineno'] == 123
    assert resp.json['break']['local_vars'] == dict(
        foo='bar',
        eggs='spam',
    )


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

    resp = testapp.post_json(
        '/sessions/{}/breaks'.format(sid),
        dict(
            lineno=123,
            file_id=file_id,
            local_vars=dict(
                foo='bar',
                eggs='spam',
            ),
        ),
        status=201,
    )
    break_ = resp.json['break']

    resp = testapp.get('/breaks/{}'.format(break_['id']))
    assert resp.json['break'] == break_
