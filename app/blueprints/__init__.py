from flask import Flask

from .main import main_bp
from .auth import auth_bp
from .dashboard import dashboard_bp
from .planner import planner_bp
from .community import community_bp

blueprints = [main_bp, auth_bp, dashboard_bp, planner_bp, community_bp]


def register_blueprints(app: Flask):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
