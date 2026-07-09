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

bp = Blueprint('units', __name__, url_prefix="/units")


bp.route("/", methods=["GET"])
def index():
    db = get_db()
    units = db.execute(
        'SELECT id, name'
        ' FROM units'
    ).fetchall()

    return render_template("units/index.html", units=units)

bp.route("/create", methods=["GET", "POST"])
def create():
    # TODO: page for creating a new unit record
    pass

bp.route("/<int:id>", methods=["GET", "PUT", "DELETE"])   # use put instead of post: we want to overwrite the existing record, not make a new one.
def modify():
    # TODO: page for editing/deleting existing unit
    pass



