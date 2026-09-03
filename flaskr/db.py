import sqlite3
import click
from flask import current_app, g
from copy import deepcopy
from flaskr.util.keywords import Keywords

# Code borrowed from https://flask.palletsprojects.com/en/stable/tutorial/database/


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

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
    for keyword in Keywords:
        db.execute("INSERT INTO keywords (id, name) VALUES (?, ?)", (keyword.value, str(keyword)))
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
    unit["keywords"] = db.execute(
        "SELECT keyword_id"
        " FROM unit_keywords"
        " WHERE unit_id = ?",
        (id,),
    ).fetchall()
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
    models = db.execute(
        "SELECT models.id AS id, models.name AS name"
        " FROM unit_models"
        " INNER JOIN models ON models.id = unit_models.model_id"
        " WHERE unit_models.unit_id = ?"
        " ORDER BY name",
        (unit_id,),
    ).fetchall()
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


# Converts a query result to a dictionary, using key_column as the primary key
def query_to_dict(record, key_column: str = "id") -> dict:

    result = {}
    if isinstance(record, sqlite3.Row):
        for key in record.keys():
            result[key] = deepcopy(record[key])
    else:
        for row in record:
            id = row[key_column]
            result[id] = query_to_dict(row, key_column)

    return result

def get_keywords():
    db = get_db()
    keywords = db.execute("SELECT * FROM keywords").fetchall()
    return keywords
