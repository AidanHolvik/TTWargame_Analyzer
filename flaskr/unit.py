from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from flaskr.db import get_db

bp = Blueprint('units', __name__, url_prefix='/units')

@bp.route('/')
def list():


    return render_template('unit/list.html')

@bp.route('/fetch')
def fetch():
    # TODO: return each unit's id and name
    db = get_db()
    units = db.execute(
        'SELECT id, name, cost ' \
        'FROM unit ' \
        'ORDER BY name ASC'
        ).fetchall()
    
    unitList = []
    for row in units:
        newRow = {}
        newRow['id'] = row['id']
        newRow['name'] = row['name']
        newRow['cost'] = row['cost']
        unitList.append(newRow)

    return jsonify(unitList)



@bp.route('/create', methods=['GET', 'POST'])
def create():
    # GET: display unit editor for new unit
    # POST: create new unit record using data from the editor
    if request.method == 'POST':
        name = request.form['name']
        cost = request.form['cost']
        db = get_db()
        error = None

        if not name:
            error = 'Unit name is required.'
        
        if error is None:
            try:
                db.execute('INSERT INTO unit (name, cost) VALUES (?,?)', (name, cost))
                db.commit()
            except db.IntegrityError:
                error = f'Unit "{name}" already exists.'
            else:
                return redirect(url_for('units.list'))
        
        flash(error, 'error')

    return render_template('unit/create.html')

@bp.route('/<int:id>', methods=['GET', 'POST'])
def update(id: int):
    # GET: populate and display unit editor from DB
    # POST: update the record(s) for the specified unit using data from the editor
    if request.method == 'POST':
        name = request.form['name']
        cost = request.form['cost']
        db = get_db()
        error = None

        if not name:
            error = 'Unit name is required'
        if error is None:
            try:
                db.execute('UPDATE unit SET name=?, cost=? WHERE id=?', (name, cost, id))
                db.commit()
            except db.IntegrityError:
                error = f'Unit "{name}" already exists.'
            else:
                return redirect(url_for('units.list'))
        flash(error, 'error')
    
    elif request.method == 'GET':
        db = get_db()
        error = None

        if error is None:
            try:
                record = db.execute(
                    'SELECT id, name, cost ' \
                    'FROM unit ' \
                    'WHERE id=?',
                    (id,)
                    ).fetchone()
            except db.DatabaseError:
                error = f'Error reading unit with id "{id}"'
            else:
                return render_template(f'unit/update.html', unit=record)
        flash(error, 'error')




@bp.route('/delete/<int:id>', methods=['GET'])
def delete(id: int):
    # POST: Delete the specified unit's record(s)
    if request.method == 'GET':
        db = get_db()
        error = None

        if error is None:
            try:
                # TODO: delete all records for assigned models
                db.execute('DELETE FROM model WHERE unit=?', (id,))
                db.execute('DELETE FROM unit WHERE id=?', (id,))
                db.commit()
            except db.DatabaseError:
                error = f'Error deleting unit with id "{id}"'
            else:
                return redirect(url_for('units.list'))
    
        flash(error, 'error')

    


