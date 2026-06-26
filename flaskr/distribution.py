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
from flaskr.db import get_db
from .util.attack_sequence import AttackSequence as Atk
from .util.roll_notation import RollNotation as Roll

bp = Blueprint("distribution", __name__, url_prefix='/dist')



@bp.route("/plot", methods=("GET", "POST"))
def plot():
    if request.method == "POST":
        weapon = {
            "attacks": Roll.toValue(request.form["attacks"]),
            "skill": int(request.form["skill"]),
            "strength": int(request.form["strength"]),
            "ap": int(request.form["ap"]),
            "damage": Roll.toValue(request.form["damage"]),
        }

        defender = {
            "toughness": int(request.form["toughness"]),
            "save": int(request.form["save"]),
        }

        damage = Atk(weapon, defender).damage()
    else:
        damage = [0.0]

    return render_template("distribution/plot.html", distribution=damage)
