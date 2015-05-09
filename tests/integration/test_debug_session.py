from __future__ import unicode_literals


def test_create_session(testapp):
    resp = testapp.post(
        '/debug-sessions',
    )
    assert resp.json['id'].startswith('DS')
