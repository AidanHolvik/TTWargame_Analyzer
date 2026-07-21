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
from flaskr.db import get_db, get_model

bp = Blueprint("model", __name__, url_prefix="/<int:unit_id>")


@bp.route("/create", methods=["GET", "POST"])
def create(unit_id):
    if request.method == "POST":
        db = get_db()
        new_id = None

        name = request.form["name"]
        movement = request.form["movement"]
        toughness = request.form["toughness"]
        save = request.form["save"]
        invuln = 7  # TODO: configure based on form controls
        health = request.form["health"]

        # TODO: put into a try..except statement
        new_id = db.execute(
            "INSERT INTO models (name, movement, toughness, save, invuln_save, health)"
            " VALUES ?,?,?,?,?,?"
            " RETURNING id",
            (name, movement, toughness, save, invuln, health),
        ).fetchone()
        db.execute(
            "INSERT INTO unit_models (unit_id, model_id, quantity) VALUES ?,?,?",
            (unit_id, new_id, 1),
        )
        db.commit()

        return redirect(url_for("model.modify", unit_id=unit_id, model_id=new_id))

    return render_template("model/create.html")


@bp.route("/<int:model_id>", methods=["GET", "POST"])
def modify(unit_id, model_id):
    model = get_model(model_id)
    db = get_db()
    # Get the model's weapons and their quantities
    weapons = db.execute(
        'SELECT weapons.id AS id, model_weapons.quantity AS quantity, weapons.name AS name, "quantity_ || weapons.id AS input_name'
        " FROM model_weapons"
        " INNER JOIN weapons ON model_weapons.weapon_id = weapons.id"
        " WHERE model_weapons.model_id = ?",
        (model_id,),
    ).fetchall()

    if request.method == "POST":
        # modify record for this model
        db.execute(
            "UPDATE models"
            " SET name=?, movement=?, tougness=?, save=?, invuln_save=?, health=?"
            " WHERE id=?",
            (
                request.form["name"],
                request.form["movement"],
                request.form["toughness"],
                request.form["save"],
                7,
                request.form["health"],
                model_id,
            ),
        )
        # modify records for the assigned weapons
        for weapon in weapons:
            db.execute(
                "UPDATE model_weapons"
                " SET quantity=?"
                " WHERE model_id=? AND weapon_id=?",
                (request.form[weapon["input_name"]], model_id, weapon["id"]),
            )
        db.commit()

    return render_template(
        "model/modify.html", unit_id=unit_id, model=model, model_weapons=weapons
    )


@bp.route("/<int:model_id>/delete", methods=["GET"])
def delete(unit_id, model_id):
    db = get_db()
    db.execute(
        "DELETE FROM models"
        " INNER JOIN unit_models ON models.id = unit_models.model_id"
        " INNER JOIN model_weapons ON models.id = model_weapons.model_id"
        " INNER JOIN weapons ON model_weapons.weapon_id = weapons.id"
        " WHERE models.id = ?",
        (model_id,),
    )
    db.commit()
    return redirect(url_for("unit.modify", unit_id=unit_id))
