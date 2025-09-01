from datetime import datetime
from app.extensions import db


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    public = db.Column(db.Boolean, default=True)

    # Foreign keys
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    origin_id = db.Column(db.Integer, db.ForeignKey("origins.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    # Stats & metadata
    stats_id = db.Column(db.Integer, db.ForeignKey("stats.id"))
    review_id = db.Column(db.Integer, db.ForeignKey("reviews.id"))

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    steps = db.relationship("Step", backref="recipe", lazy=True)
    images = db.relationship("Image", backref="recipe", lazy=True)
    videos = db.relationship("Video", backref="recipe", lazy=True)
    comments = db.relationship("Comment", backref="recipe", lazy=True)

    def __repr__(self):
        return f"<Recipe {self.name}>"
