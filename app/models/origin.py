from datetime import datetime
from app.extensions import db


class Origin(db.Model):
    __tablename__ = "origins"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country = db.Column(db.String(100))
    culture = db.Column(db.String(100))
    tribe = db.Column(db.String(100))

    recipes = db.relationship("Recipe", backref="origin", lazy=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Origin {self.country}-{self.culture}>"
