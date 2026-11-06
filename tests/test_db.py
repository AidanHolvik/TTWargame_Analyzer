import sqlite3
import pytest
import flaskr.db as dbmod
from flaskr.db import get_db

# Test whether get_db() returns the same connection within the same app context and closes it afterwards
def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT 1")

    assert "closed" in str(e.value)


# Test whether the init-db command properly executes init_db()
def test_init_db_command(runner, monkeypatch):
    # Arrange
    class Recorder(object):
        called = False
    
    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr("flaskr.db.init_db", fake_init_db)

    # Act
    result = runner.invoke(["init-db"])

    # Assert
    assert "Initialized" in result.output
    assert Recorder.called

# TODO: test_getUnits
def test_getUnit(app):
    with app.app_context():
        unit = dbmod.get_unit(1)
        assert unit is not None
        assert "id" in unit
        assert "name" in unit
        assert unit["id"] == 1
        assert unit["name"] == 'Unit 1'
        
def test_getUnit_nonexistent(app):
    with app.app_context():
        unit = dbmod.get_unit(9999)
        assert unit is None
        
# TODO: test_getModel
# TODO: test_getWeapon
# TODO: test_listUnitModels
# TODO: test_getUnitWeapons
# TODO: test_queryToDict_goodInputs
# TODO: test_queryToDict_missingRecord
# TODO: test_queryToDict_badRecord
# TODO: test_queryToDict_badKey

# TODO: test invalid/valid entries to the database?