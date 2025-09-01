from datetime import datetime
from app.extensions import db


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Integer)  # rating 1–5
    description = db.Column(db.Text)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Review {self.value}>"
