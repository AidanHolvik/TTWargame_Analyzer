import sqlite3
import click
from flask import current_app, g

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
        db.executescript(file.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_unit(id:int):
    db = get_db()
    unit = db.execute("SELECT name" " FROM units" " WHERE id=?", (id,)).fetchone()
    return unit


def get_model(id:int):
    db = get_db()
    model = db.execute(
        "SELECT name, movement, toughness, save, invuln_save, health"
        " FROM models"
        " WHERE id=?",
        (id,),
    ).fetchone()
    return model


def get_weapon(id:int):
    db = get_db()
    weapon = db.execute(
        "SELECT name, attacks, skill, strength, ap, damage"
        " FROM weapons"
        " WHERE id=?",
        (id,),
    )
    return weapon

def roll_pattern() -> str:
    return "^\d+(?i:D\d+)?(\+\d+)?$|^(?i:D\d+)(\+\d+)?$"
