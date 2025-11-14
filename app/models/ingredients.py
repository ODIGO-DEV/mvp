from datetime import datetime
from app.extensions import db


class Ingredient(db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    unit = db.Column(db.String(50))  # teaspoon, cup, gram, etc.
    quantity = db.Column(db.Float)
    notes = db.Column(db.String(255))  # optional notes
    image_url = db.Column(db.String(255))

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"))

    public = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    images = db.relationship("Image", backref="ingredient", lazy=True, foreign_keys="Image.ingredient_id")

    def __repr__(self):
        return f"<Ingredient {self.quantity} {self.unit} {self.name}>"
