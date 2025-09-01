from datetime import datetime
from app.extensions import db


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment_text = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Comment {self.comment_text[:20]}>"
