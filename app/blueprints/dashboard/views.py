from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.recipe import Recipe
from app.models.category import Category
from app.models.origin import Origin
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.extensions import db
from sqlalchemy import or_, desc
from app.blueprints.dashboard.forms import AddRecipeForm
from app.models.step import Step
from app.models.ingredients import Ingredient
from app.models.image import Image
from app.services.upload import upload_service
from datetime import datetime

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

    # Get current hour for greeting
    current_hour = datetime.now().hour

    # Get recent community activity
    recent_posts = Post.query.order_by(desc(Post.created_at)).limit(5).all()
    recent_comments = Comment.query.order_by(desc(Comment.created_at)).limit(5).all()

    # Recommended recipes (simple version)
    recommended_recipes = Recipe.query.filter(Recipe.public == True).order_by(db.func.random()).limit(4).all()

    return render_template("dashboard/index.html",
                         user_recipes=user_recipes,
                         recent_recipes=recent_recipes,
                         categories=categories,
                         origins=origins,
                         total_recipes=total_recipes,
                         total_public_recipes=total_public_recipes,
                         current_hour=current_hour,
                         recent_posts=recent_posts,
                         recent_comments=recent_comments,
                         recommended_recipes=recommended_recipes)

@dashboard_bp.route("/my-recipes")
@login_required
def my_recipes():
    page = request.args.get('page', 1, type=int)
    per_page = 9
    category_id = request.args.get('category', type=int)
    visibility = request.args.get('visibility', 'all')
    sort_by = request.args.get('sort_by', 'date_desc')

    query = Recipe.query.filter_by(user_id=current_user.id)

    if category_id:
        query = query.filter_by(category_id=category_id)

    if visibility == 'public':
        query = query.filter_by(public=True)
    elif visibility == 'private':
        query = query.filter_by(public=False)

    if sort_by == 'date_asc':
        query = query.order_by(Recipe.created_at.asc())
    elif sort_by == 'name_asc':
        query = query.order_by(Recipe.name.asc())
    elif sort_by == 'name_desc':
        query = query.order_by(Recipe.name.desc())
    else:
        query = query.order_by(desc(Recipe.created_at))

    recipes = query.paginate(
        page=page, per_page=per_page, error_out=False
    )

    categories = Category.query.all()

    return render_template("dashboard/my_recipes.html", 
                         recipes=recipes, 
                         categories=categories,
                         current_category=category_id,
                         current_visibility=visibility,
                         current_sort_by=sort_by)

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

            # Handle main recipe image (optional)
            if form.recipe_image.data:
                ok, url = upload_service.upload_file(form.recipe_image.data)
                if ok and url:
                    db.session.add(Image(url=url, recipe_id=recipe.id))

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

            # Handle step images if any (store as additional recipe images)
            step_images = request.files.getlist('step_images[]')
            for file_storage in step_images:
                if getattr(file_storage, 'filename', ''):
                    ok, url = upload_service.upload_file(file_storage)
                    if ok and url:
                        db.session.add(Image(url=url, recipe_id=recipe.id))

            db.session.commit()
            flash("Recipe created successfully!", "success")
            return redirect(url_for("dashboard.my_recipes"))

        except Exception as e:
            db.session.rollback()
            flash("An error occurred while creating the recipe. Please try again.", "error")

    return render_template("dashboard/add_recipe.html", form=form)

@dashboard_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    form = SettingsForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Settings updated successfully!", "success")
        return redirect(url_for('dashboard.settings'))
    return render_template("dashboard/settings.html", form=form)
