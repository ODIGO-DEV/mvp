from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.meal import MealPlan, MealEntry
from app.models.recipe import Recipe
from app.models.ingredients import Ingredient
from app.services.nutrition import estimate_recipe_macros, score_recipe_for_goal
from app.blueprints.planner.forms import MealPlannerForm


planner_bp = Blueprint("planner", __name__, url_prefix="/planner")


def _get_or_create_plan(user_id: int, plan_date: date) -> MealPlan:
    plan = MealPlan.query.filter_by(user_id=user_id, plan_date=plan_date).first()
    if not plan:
        plan = MealPlan(user_id=user_id, plan_date=plan_date)
        db.session.add(plan)
        db.session.commit()
    return plan


@planner_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    # pick date from query or today
    date_str = request.values.get("date")
    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()
    except ValueError:
        selected_date = date.today()

    form = MealPlannerForm()
    if form.validate_on_submit():
        plan = _get_or_create_plan(current_user.id, selected_date)
        # Clear existing entries for simplicity
        MealEntry.query.filter_by(meal_plan_id=plan.id).delete()
        db.session.flush()

        for meal_type in ["breakfast", "lunch", "dinner"]:
            rid = request.form.get(meal_type + "_recipe_id")
            if rid:
                try:
                    rid = int(rid)
                except ValueError:
                    rid = None
            if rid:
                db.session.add(MealEntry(meal_plan_id=plan.id, meal_type=meal_type, recipe_id=rid))
        db.session.commit()
        flash("Meal plan updated", "success")
        return redirect(url_for("planner.index", date=selected_date.isoformat()))

    # Load plan
    plan = MealPlan.query.filter_by(user_id=current_user.id, plan_date=selected_date).first()
    entries = {e.meal_type: e for e in (plan.entries if plan else [])}

    # Recipes for selection
    recipes = Recipe.query.filter((Recipe.public == True) | (Recipe.user_id == current_user.id)).order_by(Recipe.name).all()

    # Nutrition totals
    totals = {"protein": 0.0, "carbs": 0.0, "fats": 0.0, "calories": 0.0}
    selected_recipes = []
    if plan:
        for e in plan.entries:
            r = Recipe.query.get(e.recipe_id)
            if r:
                selected_recipes.append((e.meal_type, r))
                m = estimate_recipe_macros(r)
                for k in totals:
                    totals[k] += m[k]

    return render_template(
        "planner/index.html",
        selected_date=selected_date,
        entries=entries,
        recipes=recipes,
        totals=totals,
        selected_recipes=selected_recipes,
        form=form,
    )


@planner_bp.route("/grocery-list")
@login_required
def grocery_list():
    date_str = request.args.get("date")
    selected_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()
    plan = MealPlan.query.filter_by(user_id=current_user.id, plan_date=selected_date).first()
    items = {}
    if plan:
        for e in plan.entries:
            r = Recipe.query.get(e.recipe_id)
            if not r:
                continue
            for ing in r.ingredients:
                key = (ing.name or "").strip().lower(), (ing.unit or "").strip().lower()
                qty = float(ing.quantity or 0)
                items.setdefault(key, 0.0)
                items[key] += qty
    # Transform for template
    aggregated = [
        {"name": k[0], "unit": k[1], "quantity": v}
        for k, v in sorted(items.items())
    ]
    return render_template("planner/grocery_list.html", selected_date=selected_date, items=aggregated)


@planner_bp.route("/suggestions")
@login_required
def suggestions():
    goal = (request.args.get("goal") or "").lower().replace(" ", "_")
    if goal not in ("high_protein", "low_carb", "balanced"):
        goal = "balanced"
    recipes = Recipe.query.filter((Recipe.public == True) | (Recipe.user_id == current_user.id)).all()
    scored = sorted(((r, score_recipe_for_goal(r, goal)) for r in recipes), key=lambda x: x[1], reverse=True)
    # top 10
    scored = [(r, s) for r, s in scored[:10]]
    return render_template("planner/suggestions.html", goal=goal, scored=scored)

