from datetime import datetime
from app.extensions import db


class Stat(db.Model):
    __tablename__ = "stats"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(50))  # like, dislike, view
    value = db.Column(db.Integer, default=0)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Stat {self.type}:{self.value}>"
