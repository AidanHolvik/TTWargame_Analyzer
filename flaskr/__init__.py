"""
Two Roles:
    - Contains application factory
    - tells python to treat the flaskr directory as a package
"""

import os
from flask import Flask, g, redirect, render_template, url_for


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite")
    )  # TODO: change secret key and database path for production?

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # enforce that the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # g.root_url = 'http://localhost:5000'
    # Initialize the database
    from . import db
    db.init_app(app)

    # Register blueprints
    from . import unit
    from . import model
    from . import weapon
    from . import distribution
    app.register_blueprint(unit.bp)
    app.register_blueprint(model.bp)
    app.register_blueprint(weapon.bp)
    app.register_blueprint(distribution.bp)

    # from . import tests
    # app.register_blueprint(tests.bp)



    # set default route for testing and debug purposes
    @app.route('/')
    def default_page():
        return redirect(
            url_for('unit.index')
        )  # TODO: change this to something more useful for production

    return app
