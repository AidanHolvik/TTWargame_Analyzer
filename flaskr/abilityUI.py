from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
)
from flaskr.db import get_db, get_keywords
# from flaskr.util.abilities import (
#     WeaponAbilityType,
#     WeaponAbility,
#     WeaponAbilityValued,
#     WeaponAbilityKeyworded,
#     ModelAbilityType,
#     ModelAbility,
#     ModelAbilityValued,
# )


bp = Blueprint("ability", __name__, url_prefix="/ability")

@bp.route("/create", methods=["GET", "POST"])
def create(unit_id, model_id = None, weapon_id = None):
    if request.method == "POST":
        # Handle form submission here
        data = request.form
        # Example: process the data and save the ability
        # You would replace this with your actual logic
        flash("Ability created successfully.")
        # TODO: redirect to owner's modify page
    keywords = get_keywords()
    # TODO: set return destination based on owner type/id
    if (weapon_id):
        return_dest = url_for("weapon.modify", unit_id=unit_id, model_id=model_id, weapon_id=weapon_id)
    elif (model_id):
        return_dest = url_for("model.modify", unit_id=unit_id, model_id=model_id)
    else:
        return_dest = url_for("unit.modify", unit_id=unit_id)
    return render_template("ability/create.html", return_url=return_dest, keywords=keywords)