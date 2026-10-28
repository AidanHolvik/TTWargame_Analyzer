import sqlite3
import pytest
from flaskr.db import get_db

def test_get_close_db(app):
    # get_db should return the same connection every time it is called within the same app context
    with app.app_context():
        db = get_db()
        assert db is get_db()
    
    # after the context, the database connection should be closed
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT 1")
    assert "closed" in str(e.value)

def test_init_db_command(runner, monkeypatch):
    # Tracks whether init_db was called
    class Recorder(object):
        called = False
    
    # stand-in for init_db()
    def fake_init_db():
        Recorder.called = True

    # the command for initializing the database should call init_db
    monkeypatch.setattr("flaskr.db.init_db", fake_init_db)
    result = runner.invoke(["init-db"])
    assert "Initialized" in result.output
    assert Recorder.called