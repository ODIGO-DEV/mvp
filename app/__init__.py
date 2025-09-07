from flask import Flask
from flask_login import LoginManager

from app.extensions import db, migrate, csrf
from app.blueprints import register_blueprints
from app.models import User


def create_app(config_object="app.core.config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        from app import models

        db.create_all()

    # Register blueprints
    register_blueprints(app)
    return app
