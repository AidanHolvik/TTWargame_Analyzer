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
from flaskr.db import get_db

bp = Blueprint("unit", __name__)


@bp.route("/units", methods=["GET"])
def index():
    db = get_db()
    units = db.execute("SELECT id, name" " FROM units").fetchall()

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

        return redirect(url_for("unit.update", unit_id=new_id))

    return render_template("unit/create.html")


@bp.route("/<int:unit_id>", methods=("GET", "POST"))
def update(unit_id):
    # TODO: page for editing/deleting existing unit
    pass


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
