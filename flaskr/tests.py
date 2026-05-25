from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify

bp = Blueprint('tests', __name__, url_prefix='/tests')


@bp.route('/plot')
def plot():
    return render_template('tests/plot.html')
