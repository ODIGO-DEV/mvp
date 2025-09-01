from flask import Flask

from .main.views import main_bp


blueprints = [main_bp]


def register_blueprints(app: Flask):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
