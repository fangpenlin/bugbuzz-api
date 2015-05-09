from __future__ import unicode_literals
import urllib


def test_event_reading(testapp, session, session2):
    # Create other events, ensure we will get only events for our own session
    sid2 = session['id']
    testapp.post('/sessions/{}/actions/{}'.format(sid2, 'next'))

    sid = session['id']
    created_events = []
    for command in ['next', 'step', 'continue']:
        resp = testapp.post('/sessions/{}/actions/{}'.format(sid, command))
        created_events.append(resp.json)
    resp = testapp.get('/sessions/{}/events'.format(sid))
    assert resp.json['events'] == created_events

    def get_events(last_timestamp):
        return testapp.get(
            '/sessions/{}/events?{}'
            .format(sid, urllib.urlencode(dict(last_timestamp=last_timestamp)))
        )

    resp = get_events(created_events[0]['created_at'])
    assert resp.json['events'] == created_events[1:]

    resp = get_events(created_events[1]['created_at'])
    assert resp.json['events'] == created_events[2:]

    resp = get_events(created_events[2]['created_at'])
    assert resp.json['events'] == []
