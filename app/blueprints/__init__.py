from flask import Flask

from .main import main_bp
from .auth import auth_bp

blueprints = [main_bp, auth_bp]


def register_blueprints(app: Flask):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
