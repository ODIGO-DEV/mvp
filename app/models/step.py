from datetime import datetime
from app.extensions import db


class Step(db.Model):
    __tablename__ = "steps"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    step_number = db.Column(db.Integer, nullable=False)
    instruction = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Integer)  # duration in minutes
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    video_point = db.Column(db.String(100))  # timestamp marker

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    tasks = db.relationship("Task", backref="step", lazy=True)
    images = db.relationship("Image", backref="step", lazy=True, foreign_keys="Image.step_id")

    def __repr__(self):
        return f"<Step {self.step_number}: {self.instruction[:50]}>"
