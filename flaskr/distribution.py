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
from flaskr.db import get_db, get_model, get_units, get_unit_weapons, list_unit_models, query_to_dict, get_unit
from copy import deepcopy
from .util.attack_sequence import UnitAttackSequence as Atk
from .util.roll_notation import RollNotation as Roll

bp = Blueprint("distribution", __name__, url_prefix="/plot")

@bp.route("/<int:attacker_id>", methods=["GET"])
def plot(attacker_id):
    db = get_db()
    defender_id = request.args.get("defender")
    selection = request.args.getlist("selected_weapons")

    weapons = query_to_dict(get_unit_weapons(attacker_id), 'id')
    selected_weapons = {}
    for weapon_id in selection:
        selected_weapons[int(weapon_id)] = weapons[int(weapon_id)]

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
    return render_template(
        "distribution/plot.html", units=units, attacker=attacker, models=models, weapons=weapons, selected_weapons=selected_weapons, distribution=damage, defender=defender_id
    )
