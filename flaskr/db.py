import sqlite3
import click
from flask import current_app, g
from copy import deepcopy
from enum import Enum

# Code borrowed from https://flask.palletsprojects.com/en/stable/tutorial/database/

# Borrowed from https://docs.python.org/3/library/sqlite3.html#sqlite3-howto-row-factory
def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def list_factory(cursor, row): # Should only be used when you are retrieving an individual value from each row
    return row[0]

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = dict_factory
        # g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as file:
        db.executescript(file.read().decode("utf-8"))

    # Initialize keywords from the Keyword enum (flaskr/util/keywords.py)
    for keyword in Keyword:
        db.execute("INSERT INTO keywords (id, name) VALUES (?, ?)", (keyword.value, str(keyword)))
    # Initialize abilities
    db.execute("INSERT INTO abilities (effect) VALUES"
               "('Feel No Pain'),"
               "('AP on crit wound'),"
               "('FNP on psychic'),"
               "('FNP on mortal wounds'),"
               "('-1 to wound on strong attacks'),"
               "('ANTI-'),"
               "('BLAST/CLEAVE'),"
               "('CLOSE QUARTERS'),"
               "('DEVASTATING WOUNDS'),"
               "('INDIRECT FIRE'),"
               "('LETHAL HITS'),"
               "('MELTA'),"
               "('PSYCHIC'),"
               "('RAPID FIRE'),"
               "('SUSTAINED HITS'),"
               "('TORRENT'),"
               "('TWIN-LINKED'),"
               "('CONVERSION');")
    db.commit()
    


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_units():
    db = get_db()
    units = db.execute("SELECT * FROM units").fetchall()
    return units


def get_unit(id: int):
    db = get_db()
    unit = db.execute("SELECT * FROM units WHERE id=?", (id,)).fetchone()
    cur = db.cursor()
    cur.row_factory = list_factory
    unit["keywords"] = cur.execute(
        "SELECT keyword_id"
        " FROM unit_keywords"
        " WHERE unit_id = ?",
        (id,),
    ).fetchall()
    cur.close()
    return unit


def get_model(id: int):
    db = get_db()
    model = db.execute(
        "SELECT * FROM models WHERE id=?",
        (id,),
    ).fetchone()
    return model


def get_weapon(id: int):
    db = get_db()
    weapon = db.execute(
        "SELECT * FROM weapons WHERE id=?",
        (id,),
    ).fetchone()
    return weapon


def list_unit_models(unit_id: int):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = list_factory
    models = cur.execute(
        "SELECT models.id AS id, models.name AS name"
        " FROM unit_models"
        " INNER JOIN models ON models.id = unit_models.model_id"
        " WHERE unit_models.unit_id = ?"
        " ORDER BY name",
        (unit_id,),
    ).fetchall()
    cur.close()
    return models


def get_unit_weapons(unit_id: int):
    db = get_db()
    weapons = db.execute(
        "SELECT weapons.id AS id, unit_models.quantity * model_weapons.quantity AS quantity, weapons.name AS name, weapons.attacks AS attacks,"
        " weapons.skill AS skill, weapons.strength AS strength, weapons.ap AS ap, weapons.damage AS damage"
        " FROM unit_models"
        " INNER JOIN models ON models.id = unit_models.model_id"
        " INNER JOIN model_weapons ON model_weapons.model_id = models.id"
        " INNER JOIN weapons ON weapons.id = model_weapons.weapon_id"
        " WHERE unit_models.unit_id = ?",
        (unit_id,),
    ).fetchall()

    return weapons


def roll_pattern() -> str:
    return "^\\d+(?i:D\\d+)?(\\+\\d+)?$|^(?i:D\\d+)(\\+\\d+)?$"


# # Converts a query result to a dictionary, using key_column as the primary key
def query_to_dict(record, key_column: str = "id") -> dict:

    result = {}
    if isinstance(record, dict):
        result = record
    else:
        for row in record:
            id = row[key_column]
            result[id] = query_to_dict(row, key_column)

    return result

def get_keywords():
    db = get_db()
    keywords = db.execute("SELECT * FROM keywords").fetchall()
    return keywords

class Keyword(Enum):
    BATTLELINE = 1
    SWARM = 2
    INFANTRY = 3
    BEAST = 4
    MOUNTED = 5
    MONSTER = 6
    VEHICLE = 7
    AIRCRAFT = 8
    FRAME = 9

    CHARACTER = 10
    EPIC_HERO = 11
    WALKER = 12
    TITANIC = 13
    TOWERING = 14
    FORTIFICATION = 15
    PSYKER = 16
    ARTILLERY = 17

    GRENADES = 18
    SMOKE = 19
    FLY = 20
    TRANSPORT = 21
    DEDICATED_TRANSPORT = 22

    IMPERIUM = 23
    CHAOS = 24
    DAEMON = 25

    def __str__(self):
        match self:
            case Keyword.BATTLELINE:
                return "BATTLELINE"
            case Keyword.SWARM:
                return "SWARM"
            case Keyword.INFANTRY:
                return "INFANTRY"
            case Keyword.BEAST:
                return "BEAST"
            case Keyword.MOUNTED:
                return "MOUNTED"
            case Keyword.MONSTER:
                return "MONSTER"
            case Keyword.VEHICLE:
                return "VEHICLE"
            case Keyword.AIRCRAFT:
                return "AIRCRAFT"
            case Keyword.FRAME:
                return "FRAME"

            case Keyword.CHARACTER:
                return "CHARACTER"
            case Keyword.EPIC_HERO:
                return "EPIC HERO"
            case Keyword.WALKER:
                return "WALKER"
            case Keyword.TITANIC:
                return "TITANIC"
            case Keyword.TOWERING:
                return "TOWERING"
            case Keyword.FORTIFICATION:
                return "FORTIFICATION"
            case Keyword.PSYKER:
                return "PSYKER"

            case Keyword.GRENADES:
                return "GRENADES"
            case Keyword.SMOKE:
                return "SMOKE"
            case Keyword.FLY:
                return "FLY"
            case Keyword.TRANSPORT:
                return "TRANSPORT"
            case Keyword.DEDICATED_TRANSPORT:
                return "DEDICATED TRANSPORT"

            case Keyword.IMPERIUM:
                return "IMPERIUM"
            case Keyword.CHAOS:
                return "CHAOS"
            case Keyword.DAEMON:
                return "DAEMON"
            case _:
                return "ERROR"