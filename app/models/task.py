from datetime import datetime
from app.extensions import db


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timer = db.Column(db.Integer)  # seconds/minutes

    step_id = db.Column(db.Integer, db.ForeignKey("steps.id"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.timer}s>"
