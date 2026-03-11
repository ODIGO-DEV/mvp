from datetime import datetime
from app.extensions import db


class ShoppingListItem(db.Model):
    __tablename__ = "shopping_list_items"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.String(50))  # e.g., "2 lbs", "3 pieces", etc.
    category = db.Column(db.String(50))  # e.g., "Produce", "Dairy", "Meat", etc.
    checked = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to user
    user = db.relationship("User", backref="shopping_items")

    def __repr__(self):
        return f"<ShoppingListItem {self.name}>"
