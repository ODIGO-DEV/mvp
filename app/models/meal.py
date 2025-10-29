from datetime import date, datetime
from app.extensions import db


class MealPlan(db.Model):
    __tablename__ = "meal_plans"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    plan_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    entries = db.relationship("MealEntry", backref="meal_plan", lazy=True, cascade="all, delete-orphan")

    __table_args__ = (
        db.UniqueConstraint("user_id", "plan_date", name="uq_user_date"),
    )

    def __repr__(self):
        return f"<MealPlan {self.user_id} {self.plan_date}>"


class MealEntry(db.Model):
    __tablename__ = "meal_entries"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meal_plan_id = db.Column(db.Integer, db.ForeignKey("meal_plans.id"), nullable=False)
    meal_type = db.Column(db.String(20), nullable=False)  # breakfast, lunch, dinner
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<MealEntry {self.meal_type} recipe={self.recipe_id}>"

