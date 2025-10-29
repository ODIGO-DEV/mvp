from flask import Blueprint, render_template, send_from_directory, current_app
from flask_login import login_required

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/uploads/<path:filename>")
def uploaded_file(filename):
    """Serve user-uploaded files from the configured upload folder."""
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
