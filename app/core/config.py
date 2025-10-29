import os

SECRET_KEY = os.environ.get("SECRET_KEY", "a_default_secret_key")
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL", "sqlite:///../instance/app.db"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# File uploads
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
DEFAULT_UPLOAD_DIR = os.path.join(INSTANCE_DIR, "uploads")
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", DEFAULT_UPLOAD_DIR)
MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))

# Google OAuth
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
