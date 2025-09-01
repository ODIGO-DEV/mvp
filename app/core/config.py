import os

SECRET_KEY = os.environ.get("SECRET_KEY", "a_default_secret_key")
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///../instance/app.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Google OAuth
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
