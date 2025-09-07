from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.recipe import Recipe
from app.models.category import Category
from app.models.origin import Origin
from app.models.user import User
from app.extensions import db
from sqlalchemy import or_, desc
from app.blueprints.dashboard.forms import AddRecipeForm
from app.models.step import Step
from app.models.ingredients import Ingredient

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/")
@login_required
def index():
    # Get user's recipes
    user_recipes = Recipe.query.filter_by(user_id=current_user.id).order_by(desc(Recipe.created_at)).limit(6).all()

    # Get recent recipes from other users (excluding current user's recipes)
    recent_recipes = Recipe.query.filter(Recipe.user_id != current_user.id, Recipe.public == True).order_by(desc(Recipe.created_at)).limit(12).all()

    # Get categories for filtering
    categories = Category.query.all()
    origins = Origin.query.all()

    # Get stats
    total_recipes = Recipe.query.filter_by(user_id=current_user.id).count()
    total_public_recipes = Recipe.query.filter_by(public=True).count()

    return render_template("dashboard/index.html",
                         user_recipes=user_recipes,
                         recent_recipes=recent_recipes,
                         categories=categories,
                         origins=origins,
                         total_recipes=total_recipes,
                         total_public_recipes=total_public_recipes)

@dashboard_bp.route("/my-recipes")
@login_required
def my_recipes():
    page = request.args.get('page', 1, type=int)
    per_page = 9

    recipes = Recipe.query.filter_by(user_id=current_user.id).order_by(desc(Recipe.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template("dashboard/my_recipes.html", recipes=recipes)

@dashboard_bp.route("/explore")
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    origin_id = request.args.get('origin', type=int)
    search = request.args.get('search', '')
    per_page = 12

    # Build query
    query = Recipe.query.filter(Recipe.public == True)

    if category_id:
        query = query.filter_by(category_id=category_id)

    if origin_id:
        query = query.filter_by(origin_id=origin_id)

    if search:
        query = query.filter(or_(
            Recipe.name.contains(search),
            Recipe.description.contains(search)
        ))

    recipes = query.order_by(desc(Recipe.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )

    categories = Category.query.all()
    origins = Origin.query.all()

    return render_template("dashboard/explore.html",
                         recipes=recipes,
                         categories=categories,
                         origins=origins,
                         current_category=category_id,
                         current_origin=origin_id,
                         current_search=search)

@dashboard_bp.route("/recipe/<int:recipe_id>")
@login_required
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    # Check if user can view this recipe
    if not recipe.public and recipe.user_id != current_user.id:
        return render_template("dashboard/error.html", message="Recipe not found or not accessible"), 404

    return render_template("dashboard/recipe_detail.html", recipe=recipe)

@dashboard_bp.route("/add-recipe", methods=["GET", "POST"])
@login_required
def add_recipe():
    form = AddRecipeForm()

    if form.validate_on_submit():
        try:
            # Create the recipe
            recipe = Recipe(
                name=form.name.data,
                description=form.description.data,
                public=form.public.data,
                user_id=current_user.id,
                category_id=form.category_id.data if form.category_id.data != 0 else None,
                origin_id=form.origin_id.data if form.origin_id.data != 0 else None
            )

            db.session.add(recipe)
            db.session.flush()  # Get the recipe ID

            # Parse ingredients from request
            ingredient_names = request.form.getlist('ingredient_names[]')
            ingredient_quantities = request.form.getlist('ingredient_quantities[]')
            ingredient_units = request.form.getlist('ingredient_units[]')
            ingredient_notes = request.form.getlist('ingredient_notes[]')

            for i, name in enumerate(ingredient_names):
                if name.strip():  # Only add if name is provided
                    ingredient = Ingredient(
                        name=name.strip(),
                        quantity=float(ingredient_quantities[i]) if i < len(ingredient_quantities) and ingredient_quantities[i] and ingredient_quantities[i].strip() else None,
                        unit=ingredient_units[i].strip() if i < len(ingredient_units) and ingredient_units[i] else None,
                        notes=ingredient_notes[i].strip() if i < len(ingredient_notes) and ingredient_notes[i] else None,
                        recipe_id=recipe.id,
                        user_id=current_user.id
                    )
                    db.session.add(ingredient)

            # Parse steps from request
            step_numbers = request.form.getlist('step_numbers[]')
            step_names = request.form.getlist('step_names[]')
            step_instructions = request.form.getlist('step_instructions[]')
            step_durations = request.form.getlist('step_durations[]')
            step_descriptions = request.form.getlist('step_descriptions[]')

            for i, instruction in enumerate(step_instructions):
                if instruction.strip():  # Only add if instruction is provided
                    step = Step(
                        step_number=int(step_numbers[i]) if i < len(step_numbers) and step_numbers[i] and step_numbers[i].strip() else i+1,
                        name=step_names[i].strip() if i < len(step_names) and step_names[i] else None,
                        instruction=instruction.strip(),
                        duration=int(step_durations[i]) if i < len(step_durations) and step_durations[i] and step_durations[i].strip() else None,
                        description=step_descriptions[i].strip() if i < len(step_descriptions) and step_descriptions[i] else None,
                        recipe_id=recipe.id
                    )
                    db.session.add(step)

            db.session.commit()
            flash("Recipe created successfully!", "success")
            return redirect(url_for("dashboard.my_recipes"))

        except Exception as e:
            db.session.rollback()
            flash("An error occurred while creating the recipe. Please try again.", "error")

    return render_template("dashboard/add_recipe.html", form=form)
