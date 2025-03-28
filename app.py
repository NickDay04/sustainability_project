# -*- coding: utf-8 -*-
"""
    app.py
    ~~~~~~

    Initializes a Flask application with SQLite database configuration and SQLAlchemy setup.
    Registers blueprints for handling user-related and main page routes. Starts the Flask application.

    :copyright: (c) 2024 by Newcastle University CSC2033 Team 8.
    :license: see LICENSE.MD for more details.
"""

from functools import wraps
import os
import secrets
from dotenv import load_dotenv

from flask import Flask, render_template, session
from flask_login import LoginManager, current_user, login_user
from flask_qrcode import QRcode

from extensions import db

try:
    load_dotenv()
except RuntimeError:
    raise FileNotFoundError(".env does not exist to be loaded from.")

# setup app
app = Flask(__name__)
app.debug = os.getenv("APP_DEBUGGING")
app.config['SECRET_KEY'] = secrets.token_hex(16)

# setup database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://" \
                                        + os.getenv("MYSQL_USER") \
                                        + ":" \
                                        + os.getenv("MYSQL_PASSWORD") \
                                        + "@" \
                                        + os.getenv("MYSQL_HOST") \
                                        + "/dev"

# init app before running & populate db if possible.
db.init_app(app)
with app.app_context():
    db.create_all()

qrcode = QRcode(app)

# Set up login manager
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.init_app(app)


@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def forbidden_error():
    return render_template('errors/403.html'), 403


@app.errorhandler(400)
def bad_request_error(error):
    return render_template('errors/400.html'), 400


@app.errorhandler(503)
def service_unavailable(error):
    return render_template('errors/503.html'), 503


@login_manager.user_loader
def load_user(id):
    return db.session.get(User, id)


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                return render_template("error/403.html")
            return f(*args, **kwargs)

        return wrapped

    return wrapper


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=secrets.token_hex(16),
        SQLALCHEMY_DATABASE_URI="mysql+pymysql://" \
            + os.getenv("MYSQL_USER") \
            + ":" \
            + os.getenv("MYSQL_PASSWORD") \
            + "@" \
            + os.getenv("MYSQL_HOST") \
            + "/dev"
    )
    if config:
        app.config.update(config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    login_manager.init_app(app)

    from users.views import users_blueprint
    from main.views import index_blueprint
    from activities.views import activities_blueprint

    app.register_blueprint(users_blueprint)
    app.register_blueprint(index_blueprint)
    app.register_blueprint(activities_blueprint)

    return app


if __name__ == '__main__':
    from users.views import users_blueprint
    from main.views import index_blueprint
    from activities.views import activities_blueprint
    from social.views import social_blueprint
    from models import User

    app.register_blueprint(users_blueprint)
    app.register_blueprint(index_blueprint)
    app.register_blueprint(activities_blueprint)
    app.register_blueprint(social_blueprint)

    app.run()
