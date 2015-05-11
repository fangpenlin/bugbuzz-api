from __future__ import unicode_literals


def test_create_break(testapp, session):
    sid = session['id']
    resp = testapp.post(
        '/sessions/{}/breaks'.format(sid),
        dict(
            filename='foobar.py',
            lineno=123,
            # TODO: break types?
            # TODO: other info
        )
    )
    assert resp.json['id'].startswith('BK')
    assert resp.json['filename'] == 'foobar.py'
    assert resp.json['lineno'] == 123
