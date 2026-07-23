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
from flaskr.db import get_db, get_model, get_units, get_unit_weapons, list_unit_models
from .util.attack_sequence import UnitAttackSequence as Atk
from .util.roll_notation import RollNotation as Roll

bp = Blueprint("distribution", __name__, url_prefix="/dist")


@bp.route("/plot", methods=["GET"])
def plot():
    db = get_db()
    attacker_id = request.args.get("attacker")
    defender_id = request.args.get("defender")

    if attacker_id and defender_id:
        weapons = get_unit_weapons(attacker_id)
        defender = get_model(defender_id)

        # TODO: allow user to select which weapons to consider/ignore
        attacks = Atk(weapons, defender)
        damage = attacks.damage()
    else:
        damage = [0.0]

    units = get_units()
    models = {}
    for unit in units:
        models[unit["id"]] = list_unit_models(unit["id"])
    return render_template(
        "distribution/plot.html", units=units, models=models, distribution=damage
    )
