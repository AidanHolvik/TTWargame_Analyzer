from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flaskr.db import (
    get_db,
    query_to_dict,
    get_model,
    get_units,
    get_unit_weapons,
    list_unit_models,
    get_unit,
)
from copy import deepcopy
from .util.attack_sequence import UnitAttackSequence as Atk
from .util.roll_notation import RollNotation as Roll

bp = Blueprint("distribution", __name__, url_prefix="/plot")


@bp.route("/<int:attacker_id>", methods=["GET"])
def plot(attacker_id):
    db = get_db()
    defender_id = request.args.get("defender")
    selection = request.args.getlist("selected_weapons")

    # Get list of attacker's weapons, determine which are selected
    weapons = query_to_dict(get_unit_weapons(attacker_id), "id")
    selected_weapons = {}
    for weapon_id in selection:
        selected_weapons[int(weapon_id)] = weapons[int(weapon_id)]

    # propagate abilities from units/models to weapons
    for weapon in selected_weapons.values():
        abilities = db.execute(
            "SELECT * FROM propagated_abilities WHERE weapon_id = ?", (weapon["id"],)
        ).fetchall()

        if abilities:  # If abilities is not empty, add them to the weapon's abilities
            weapon["abilities"] = abilities

    if defender_id:
        defender = get_model(defender_id)

        attacks = Atk(selected_weapons, defender)
        damage = attacks.damage()
    else:
        damage = [0.0]
        selected_weapons = deepcopy(weapons)

    units = get_units()
    models = {}
    for unit in units:
        models[unit["id"]] = list_unit_models(unit["id"])
    attacker = get_unit(attacker_id)
    attacker_models = query_to_dict(list_unit_models(attacker["id"]), "id")
    for model in attacker_models.values():
        model["weapons"] = db.execute(
            "SELECT weapons.id AS id, model_weapons.quantity * unit_models.quantity AS quantity, weapons.name AS name, weapons.attacks AS attacks, weapons.skill AS skill,"
            " weapons.strength AS strength, weapons.ap AS ap, weapons.damage AS damage"
            " FROM model_weapons"
            " INNER JOIN weapons ON weapons.id = model_weapons.weapon_id"
            " INNER JOIN models ON models.id = model_weapons.model_id"
            " INNER JOIN unit_models ON unit_models.model_id = models.id"
            " WHERE models.id = ?",
            (model["id"],),
        ).fetchall()

    return render_template(
        "distribution/plot.html",
        units=units,
        attacker=attacker,
        models=models,
        weapons=weapons,
        attacker_models=attacker_models,
        selected_weapons=selected_weapons,
        distribution=damage,
        defender=defender_id,
    )
