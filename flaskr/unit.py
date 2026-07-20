from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    jsonify,
)
from flaskr.db import get_db, get_unit

bp = Blueprint("unit", __name__)


@bp.route("/units", methods=["GET"])
def index():
    db = get_db()
    units = db.execute("SELECT id, name FROM units").fetchall()

    return render_template("unit/index.html", units=units)


@bp.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        db = get_db()
        new_id = None
        name = request.form["name"]

        # TODO: put into a try..except statement
        new_id = db.execute(
            "INSERT INTO units (name) VALUES (?) RETURNING id", (name,)
        ).fetchone()
        db.commit()

        return redirect(url_for("unit.modify", unit_id=new_id))

    return render_template("unit/create.html")


@bp.route("/<int:unit_id>", methods=("GET", "POST"))
def modify(unit_id):
    unit = get_unit(unit_id)
    db = get_db()
    # Get the unit's models and their quantities
    models = db.execute(
        'SELECT models.id AS id, unit_models.quantity AS quantity, models.name AS name, "quantity_" || models.id AS input_name'
        " FROM unit_models"
        " INNER JOIN models ON unit_models.model_id = models.id"
        " WHERE unit_models.unit_id = ?",
        (unit_id,),
    ).fetchall()

    if request.method == "POST":
        # modify record for this unit
        db.execute(
            "UPDATE units" " SET name=?" " WHERE id=?", (request.form["name"], unit_id)
        )
        # modify records for this unit's models
        for model in models:
            db.execute(
                "UPDATE unit_models"
                " SET quantity=?"
                " WHERE unit_id=? AND model_id=?",
                (request.form[model["input_name"]], unit_id, model["id"]),
            )
        db.commit()

    return render_template("unit/modify.html", unit=unit, unit_models=models)


@bp.route("/<int:unit_id>/delete", methods=("DELETE"))
def delete(unit_id):
    db = get_db()
    db.execute(
        "DELETE FROM units"
        " INNER JOIN unit_models ON units.id = unit_models.unit_id"
        " INNER JOIN models ON unit_models.model_id = models.id"
        " INNER JOIN model_weapons ON models.id = model_weapons.model_id"
        " INNER JOIN weapons ON model_weapons.weapon_id = weapons.id"
        " WHERE units.id = ?",
        (id,),
    )
    db.commit()

    return redirect(url_for("unit.index"))
