from datetime import datetime
from app.extensions import db


class Preference(db.Model):
    __tablename__ = "preferences"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categories = db.Column(db.String(255))  # CSV or JSON of categories

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Preference {self.categories}>"
