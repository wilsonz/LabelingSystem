# Within an application context, /get_db()/ should return the same
# connection each time it's called. After the context, the connection
# should be closed.
import sqlite3

import pytest
from flaskr.db import get_db

def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e)


# The /init-db/ cammand should call the /init_db()/ and out a msg.
# This test use Pytest's /monkeypatch/ fixture to replace the /init_db()/
# with one that records that it's been called.
def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called
