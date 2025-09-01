from datetime import datetime
from app.extensions import db


class Step(db.Model):
    __tablename__ = "steps"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    video_point = db.Column(db.String(100))  # timestamp marker

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    tasks = db.relationship("Task", backref="step", lazy=True)

    def __repr__(self):
        return f"<Step {self.name}>"
