from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from flaskr.db import get_db

bp = Blueprint('models', __name__, url_prefix='/units/<int:unitId>/models')

@bp.route('/')
# TODO: generate HTML for visualizing a list of models + buttons in the unit editor?
def list(unitId: int):
    pass


@bp.route('/fetch')
def fetch(unitId: int):
    db = get_db()
    models = db.execute(
        'SELECT id, name, quantity, toughness, save, health, invuln, isLeader, enabled ' \
        'FROM model ' \
        'WHERE unit=? ' \
        'ORDER BY isLeader DESC, name ASC',
        (unitId,)
        ).fetchall()
    
    modelList = []
    for row in models:
        newRow = {}
        newRow['id'] = row['id']
        newRow['name'] = row['name']
        newRow['quantity'] = row['name']
        newRow['toughness'] = row['name']
        newRow['save'] = row['name']
        newRow['health'] = row['name']
        newRow['invuln'] = row['name']
        newRow['isLeader'] = row['name']
        newRow['enabled'] = row['name']
        modelList.append(newRow)

    return jsonify(modelList)




@bp.route('/create', methods=['GET','POST'])
def create(unitId: int):
    # GET: display model editor for a new model for the appropriate unit
    # POST: create new model record for the specified unit using data from the editor
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        toughness = request.form['toughness']
        save = request.form['save']
        health = request.form['health']
        invuln = request.form['invuln']
        isLeader = request.form['isLeader'] # TODO: Convert to string?
        enabled = request.form['enabled'] # TODO: Convert to string?
        db = get_db()
        error = None

        if not name:
            error = 'Model name is required.'
        
        if error is None:
            try:
                db.execute('INSERT INTO model (unit, name, quantity, toughness, save, health, invuln, isLeader, enabled)' \
                           'VALUES (?,?,?,?,?,?,?,?,?)', (unitId, name, quantity, toughness, save, health, invuln, isLeader, enabled))
                db.commit()
            except db.IntegrityError:
                error = f'Model "{name}" already exists for this unit.'
            else:
                return redirect(url_for('units.update', id=unitId))
        
        flash(error, 'error')
        
    return render_template('model/create.html')



@bp.route('/<int:modelId>', methods=['GET', 'POST'])
def update(unitId: int, modelId: int):
    # GET: populate and display unit editor from DB
    # POST: update the record(s) for the specified unit using data from the editor
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        toughness = request.form['toughness']
        save = request.form['save']
        health = request.form['health']
        invuln = request.form['invuln']
        isLeader = request.form['isLeader'] # TODO: Convert to string?
        enabled = request.form['enabled'] # TODO: Convert to string?
        db = get_db()
        error = None

        if not name:
            error = 'Unit name is required'
        if error is None:
            try:
                db.execute('UPDATE model SET name=?, quantity=?, toughness=?, save=?, health=?, invuln=?, isLeader=?, enabled=?' \
                           'WHERE id=?'
                           'VALUES (?,?,?,?,?,?,?,?,?)', (name, quantity, toughness, save, health, invuln, isLeader, enabled, modelId))
                db.commit()
            except db.IntegrityError:
                error = f'Model "{name}" already exists for this unit.'
            else:
                # TODO: either don't allow adding models in unit creator, or allow redirecting back to unit creator
                return redirect(url_for('units.update', id=int))
        flash(error, 'error')

    elif request.method == 'GET':
        db = get_db()
        error = None

        if error is None:
            try:
                record = db.execute(
                    'SELECT id, name, quantity, toughness, save, health, invuln, isLeader, enabled ' \
                    'FROM model ' \
                    'WHERE id=?',
                    (modelId,)
                    ).fetchone()
            except db.DatabaseError:
                error = f'Error reading model with id "{modelId}" for unit with id "{unitId}"'
            else:
                return render_template(f'model/update.html', model=record)
        flash(error, 'error')




@bp.route('/delete/<int:modelId>', methods=['GET'])
def delete(unitId: int, modelId: int):
    if request.method == 'GET':
        db = get_db()
        error = None

        if error is None:
            try:
                db.execute('DELETE FROM model WHERE id=?', (modelId,))
                db.commit()
            except db.DatabaseError:
                error = f'Error deleting model with id "{modelId}"'
            else:
                return redirect(url_for('units.update', id=unitId))
    
        flash(error, 'error')