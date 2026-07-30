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
from flaskr.db import get_db, get_weapon, roll_pattern

bp = Blueprint("weapon", __name__, url_prefix="/<int:unit_id>/<int:model_id>")


@bp.route("/create", methods=["GET", "POST"])
def create(unit_id, model_id):
    if request.method == "POST":
        db = get_db()
        new_id = None

        # TODO: get new record's values from form
        name = request.form["name"]
        attacks = request.form["attacks"]
        skill = request.form["skill"]
        strength = request.form["strength"]
        ap = request.form["ap"]
        damage = request.form["damage"]

        # TODO: put into a try..except statement
        new_id = db.execute(
            "INSERT INTO weapons (name, attacks, skill, strength, ap, damage)"
            " VALUES (?,?,?,?,?,?)"
            " RETURNING id",
            (name, attacks, skill, strength, ap, damage),
        ).fetchone()["id"]
        db.execute(
            "INSERT INTO model_weapons (model_id, weapon_id, quantity) VALUES (?,?,?)",
            (model_id, new_id, 1),
        )
        db.commit()

        return redirect(url_for("model.modify", unit_id=unit_id, model_id=model_id))

    return render_template(
        "weapon/create.html",
        unit_id=unit_id,
        model_id=model_id,
        roll_pattern=roll_pattern(),
    )


@bp.route("/<int:weapon_id>", methods=["GET", "POST"])
def modify(unit_id, model_id, weapon_id):
    db = get_db()

    if request.method == "POST":
        # Modify the record for this weapon
        db.execute(
            "UPDATE weapons"
            " SET name=?, attacks=?, skill=?, strength=?, ap=?, damage=?"
            " WHERE id=?",
            (
                request.form["name"],
                request.form["attacks"],
                request.form["skill"],
                request.form["strength"],
                request.form["ap"],
                request.form["damage"],
                weapon_id,
            ),
        )
        db.commit()

    weapon = get_weapon(weapon_id)
    return render_template(
        "weapon/modify.html",
        unit_id=unit_id,
        model_id=model_id,
        weapon=weapon,
        roll_pattern=roll_pattern(),
    )


@bp.route("/<int:weapon_id>/delete", methods=["GET"])
def delete(unit_id, model_id, weapon_id):
    db = get_db()
    
    db.execute("DELETE FROM model_weapons WHERE weapon_id=?", (weapon_id,))
    db.execute("DELETE FROM weapons WHERE id = ?", (weapon_id,))
    db.commit()

    return redirect(url_for("model.modify", unit_id=unit_id, model_id=model_id))
