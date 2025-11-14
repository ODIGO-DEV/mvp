from datetime import datetime
from app.extensions import db


class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), nullable=False)

    # Foreign keys - only one should be set
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.id"), nullable=True)
    step_id = db.Column(db.Integer, db.ForeignKey("steps.id"), nullable=True)

    # Image metadata
    alt_text = db.Column(db.String(255))
    caption = db.Column(db.Text)
    is_primary = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Image {self.url}>"

    @property
    def owner_type(self):
        """Return the type of entity this image belongs to"""
        if self.recipe_id:
            return 'recipe'
        elif self.ingredient_id:
            return 'ingredient'
        elif self.step_id:
            return 'step'
        return None

    @property
    def owner_id(self):
        """Return the ID of the entity this image belongs to"""
        if self.recipe_id:
            return self.recipe_id
        elif self.ingredient_id:
            return self.ingredient_id
        elif self.step_id:
            return self.step_id
        return None
