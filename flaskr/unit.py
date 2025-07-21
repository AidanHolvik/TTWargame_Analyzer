from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from flaskr.db import get_db

bp = Blueprint('units', __name__, url_prefix='/units')

@bp.route('/')
def list_units():
    return render_template('unit/list.html')

@bp.route('/fetch')
def fetch():
    # TODO: return each unit's id and name
    db = get_db()
    units = db.execute(
        'SELECT id, name ' \
        'FROM unit ' \
        'ORDER BY name ASC'
        ).fetchall()
    
    return jsonify(units)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    # GET: display unit editor for new unit
    # POST: create new unit the record(s) using data from the editor

    return render_template('unit/create.html')

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update(id: int):
    # GET: populate and display unit editor
    # POST: update the record(s) for the specified unit using data from the editor

    return render_template('unit/update.html')

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id: int):
    # POST: Delete the specified unit's record(s)
    pass


