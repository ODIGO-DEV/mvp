from flask import Flask

from .main import main_bp
from .auth import auth_bp
from .dashboard import dashboard_bp
from .planner import planner_bp
from .community import community_bp
from .shopping import shopping_bp
from .favorites import favorites_bp
from .profile import profile_bp
from .notifications import notifications_bp

blueprints = [main_bp, auth_bp, dashboard_bp, planner_bp, community_bp, shopping_bp, favorites_bp, profile_bp, notifications_bp]


def register_blueprints(app: Flask):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
