from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # auth fields
    email = db.Column(db.String(150), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)
    auth_provider = db.Column(db.String(50), default="email")
    two_factor_enabled = db.Column(db.Boolean, default=False)

    # user info
    name = db.Column(db.String(60))

    # profile info
    profile_image_url = db.Column(db.String(255))
    banner_image_url = db.Column(db.String(255))
    phone = db.Column(db.String(20), unique=True, nullable=True)
    is_verified = db.Column(db.Boolean, default=False)

    # role & status
    role = db.Column(db.String(50), default="user")
    is_active = db.Column(db.Boolean, default=True)

    # timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # relationships
    recipes = db.relationship("recipe", backref="author", lazy=True)
    collections = db.relationship("collection", backref="owner", lazy=True)
    reviews = db.relationship("review", backref="reviewer", lazy=True)
    stats = db.relationship("stat", backref="user", lazy=True)

    # helpers
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        print(self.password_hash)
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<user {self.username}>"
