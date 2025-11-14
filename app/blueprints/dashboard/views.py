from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.recipe import Recipe
from app.models.category import Category
from app.models.origin import Origin
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.extensions import db
from sqlalchemy import or_, desc, func, case
from app.blueprints.dashboard.forms import RecipeForm, CommentForm
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
    category_param = request.args.get('category')
    origin_id = request.args.get('origin', type=int)
    search = request.args.get('search', '')
    per_page = 12

    # Build query
    query = Recipe.query.filter(Recipe.public == True)

    # Handle category by ID or name
    category_id = None
    if category_param:
        try:
            # Try to parse as integer first (ID)
            category_id = int(category_param)
            query = query.filter_by(category_id=category_id)
        except ValueError:
            # If not an integer, treat as category name
            category = Category.query.filter_by(name=category_param).first()
            if category:
                category_id = category.id
                query = query.filter_by(category_id=category.id)

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
    form = CommentForm(obj=None)

    # Check if user can view this recipe
    if not recipe.public and recipe.user_id != current_user.id:
        return render_template("dashboard/error.html", message="Recipe not found or not accessible"), 404

    return render_template("dashboard/recipe_detail.html", recipe=recipe, form=form)

@dashboard_bp.route("/add-recipe", methods=["GET", "POST"])
@login_required
def add_recipe():
    form = RecipeForm(formdata=request.form, files=request.files) if request.method == 'POST' else RecipeForm()

    if request.method == 'POST':
        print(f"DEBUG: Form validation result: {form.validate()}")
        print(f"DEBUG: Form errors: {form.errors}")
        print(f"DEBUG: Request files keys: {list(request.files.keys())}")
        print(f"DEBUG: Request form keys: {list(request.form.keys())}")

    if form.validate_on_submit():
        try:
            print("DEBUG: Form validation passed, creating recipe...")
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

            # Handle recipe images - process directly from request.files
            uploaded_images = []
            print(f"DEBUG: form.recipe_images.data = {form.recipe_images.data}")
            print(f"DEBUG: request.files = {request.files}")

            # Get recipe images from request.files instead of form
            recipe_files = request.files.getlist('recipe_images')
            print(f"DEBUG: Found {len(recipe_files)} recipe files to process")
            if recipe_files:
                for file_field in recipe_files:
                    print(f"DEBUG: Processing file_field: {file_field}, type: {type(file_field)}")
                    if file_field and hasattr(file_field, 'filename') and file_field.filename:
                        print(f"DEBUG: Found valid file: {file_field.filename}")
                        # Validate file type
                        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
                        file_ext = file_field.filename.rsplit('.', 1)[1].lower() if '.' in file_field.filename else ''

                        if file_ext not in allowed_extensions:
                            flash(f"Invalid file type for {file_field.filename}. Allowed types: {', '.join(allowed_extensions)}", "error")
                            continue

                        # Validate file size (30MB max)
                        file_field.seek(0, 2)  # Seek to end
                        file_size = file_field.tell()
                        file_field.seek(0)  # Reset to beginning

                        if file_size > 30 * 1024 * 1024:  # 30MB
                            flash(f"File {file_field.filename} is too large. Maximum size is 30MB.", "error")
                            continue

                        try:
                            print(f"DEBUG: Attempting to upload {file_field.filename}")
                            ok, url = upload_service.upload_file(file_field)
                            print(f"DEBUG: Upload result - ok: {ok}, url: {url}")
                            if ok and url:
                                image = Image(url=url, recipe_id=recipe.id)
                                db.session.add(image)
                                uploaded_images.append(url)
                                print(f"DEBUG: Added image to database: {url}")
                            else:
                                flash(f"Failed to upload image: {file_field.filename}", "error")
                        except Exception as e:
                            print(f"DEBUG: Exception during upload: {str(e)}")
                            flash(f"Error uploading {file_field.filename}: {str(e)}", "error")

            if not uploaded_images:
                flash("No images were uploaded. You can add images later by editing your recipe.", "warning")

            # Handle ingredients
            for ingredient_field in form.ingredients:
                if ingredient_field.form.name.data:
                    ingredient = Ingredient(
                        name=ingredient_field.form.name.data,
                        quantity=ingredient_field.form.quantity.data,
                        unit=ingredient_field.form.unit.data,
                        notes=ingredient_field.form.notes.data,
                        recipe_id=recipe.id,
                        user_id=current_user.id
                    )
                    db.session.add(ingredient)
                    db.session.flush()  # Get ingredient ID

                    # Handle ingredient images - process directly from request.files
                    ingredient_idx = len([i for i in form.ingredients if i.form.name.data]) - 1
                    ingredient_files = request.files.getlist(f'ingredients-{ingredient_idx}-images')
                    for file_field in ingredient_files:
                        if file_field and file_field.filename:
                            try:
                                ok, url = upload_service.upload_file(file_field)
                                if ok and url:
                                    image = Image(url=url, ingredient_id=ingredient.id)
                                    db.session.add(image)
                                    print(f"DEBUG: Added ingredient image: {url}")
                            except Exception as e:
                                flash(f"Error uploading ingredient image: {str(e)}", "error")

            # Handle steps
            for step_field in form.steps:
                if step_field.form.instruction.data:
                    step = Step(
                        step_number=step_field.form.step_number.data,
                        instruction=step_field.form.instruction.data,
                        name=step_field.form.name.data if hasattr(step_field.form, 'name') else None,
                        description=step_field.form.description.data if hasattr(step_field.form, 'description') else None,
                        duration=step_field.form.duration.data if hasattr(step_field.form, 'duration') else None,
                        recipe_id=recipe.id
                    )
                    db.session.add(step)
                    db.session.flush()  # Get step ID

                    # Handle step images - process directly from request.files
                    step_idx = len([s for s in form.steps if s.form.instruction.data]) - 1
                    step_files = request.files.getlist(f'steps-{step_idx}-images')
                    for file_field in step_files:
                        if file_field and file_field.filename:
                            try:
                                ok, url = upload_service.upload_file(file_field)
                                if ok and url:
                                    image = Image(url=url, step_id=step.id)
                                    db.session.add(image)
                                    print(f"DEBUG: Added step image: {url}")
                            except Exception as e:
                                flash(f"Error uploading step image: {str(e)}", "error")

            db.session.commit()
            flash("Recipe created successfully!", "success")
            return redirect(url_for("dashboard.my_recipes"))

        except Exception as e:
            db.session.rollback()
            print(f"DEBUG: Exception in add_recipe: {str(e)}")
            print(f"DEBUG: Exception type: {type(e)}")
            import traceback
            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            flash(f"An error occurred while creating the recipe: {str(e)}", "error")
    else:
        # Form validation failed
        print(f"DEBUG: Form validation failed with errors: {form.errors}")
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", "error")

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

@dashboard_bp.route("/recipe/<int:recipe_id>/edit", methods=["GET", "POST"])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        return render_template("dashboard/error.html", message="You are not authorized to edit this recipe."), 403

    form = RecipeForm(obj=recipe)

    if form.validate_on_submit():
        try:
            recipe.name = form.name.data
            recipe.description = form.description.data
            recipe.public = form.public.data
            recipe.category_id = form.category_id.data if form.category_id.data != 0 else None
            recipe.origin_id = form.origin_id.data if form.origin_id.data != 0 else None

            # Clear existing ingredients and steps
            Ingredient.query.filter_by(recipe_id=recipe.id).delete()
            Step.query.filter_by(recipe_id=recipe.id).delete()

            # Handle main recipe image (optional)
            if form.recipe_image.data:
                ok, url = upload_service.upload_file(form.recipe_image.data)
                if ok and url:
                    # Remove old image if it exists
                    Image.query.filter_by(recipe_id=recipe.id).delete()
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

            db.session.commit()
            flash("Recipe updated successfully!", "success")
            return redirect(url_for("dashboard.my_recipes"))

        except Exception as e:
            db.session.rollback()
            flash("An error occurred while updating the recipe. Please try again.", "error")

    return render_template("dashboard/edit_recipe.html", form=form, recipe=recipe)

@dashboard_bp.route("/recipe/<int:recipe_id>/delete", methods=["GET", "POST"])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        return render_template("dashboard/error.html", message="You are not authorized to delete this recipe."), 403

    db.session.delete(recipe)
    db.session.commit()
    flash("Recipe deleted successfully!", "success")
    return redirect(url_for("dashboard.my_recipes"))

@dashboard_bp.route("/recipe/<int:recipe_id>/comment", methods=["POST"])
@login_required
def add_comment(recipe_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(comment_text=form.comment_text.data, recipe_id=recipe_id, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash("Comment posted!", "success")
    else:
        flash("Error posting comment.", "error")
    return redirect(url_for('dashboard.view_recipe', recipe_id=recipe_id))

@dashboard_bp.route("/api/ingredients/search")
@login_required
def search_ingredients():
    """API endpoint to search for existing ingredients"""
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify([])

    # Search ingredients by name, prioritizing user's own ingredients
    ingredients = db.session.query(
        Ingredient.name,
        Ingredient.unit,
        func.count(Ingredient.id).label('usage_count'),
        func.max(Ingredient.created_at).label('last_used')
    ).filter(
        or_(
            Ingredient.user_id == current_user.id,
            Ingredient.public == True
        ),
        Ingredient.name.ilike(f'%{query}%')
    ).group_by(
        Ingredient.name, Ingredient.unit
    ).order_by(
        # Prioritize user's own ingredients
        func.max(case([(Ingredient.user_id == current_user.id, 1)], else_=0)).desc(),
        func.count(Ingredient.id).desc(),  # Then by usage frequency
        func.max(Ingredient.created_at).desc()  # Then by recency
    ).limit(10).all()

    result = []
    for ingredient in ingredients:
        result.append({
            'name': ingredient.name,
            'unit': ingredient.unit or '',
            'usage_count': ingredient.usage_count,
            'display_text': f"{ingredient.name}" + (f" ({ingredient.unit})" if ingredient.unit else "")
        })

    return jsonify(result)
