from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models.favorite import Favorite
from app.models.recipe import Recipe
from app.models.category import Category
from app.models.origin import Origin
from app.extensions import db
from sqlalchemy import desc

from . import favorites_bp


@favorites_bp.route("/")
@login_required
def index():
    """Display user's favorite recipes"""
    page = request.args.get('page', 1, type=int)
    per_page = 12
    category_id = request.args.get('category', type=int)
    sort_by = request.args.get('sort_by', 'date_desc')

    # Get user's favorited recipe IDs
    favorite_ids = db.session.query(Favorite.recipe_id).filter_by(user_id=current_user.id).all()
    favorite_recipe_ids = [fav[0] for fav in favorite_ids]

    # Query recipes that are in favorites
    query = Recipe.query.filter(Recipe.id.in_(favorite_recipe_ids))

    # Apply filters
    if category_id:
        query = query.filter_by(category_id=category_id)

    # Apply sorting
    if sort_by == 'date_asc':
        query = query.order_by(Recipe.created_at.asc())
    elif sort_by == 'name_asc':
        query = query.order_by(Recipe.name.asc())
    elif sort_by == 'name_desc':
        query = query.order_by(Recipe.name.desc())
    else:  # date_desc (default)
        query = query.order_by(desc(Recipe.created_at))

    # Paginate
    recipes = query.paginate(page=page, per_page=per_page, error_out=False)

    # Get categories for filtering
    categories = Category.query.all()

    return render_template(
        "favorites/index.html",
        recipes=recipes,
        categories=categories,
        current_category=category_id,
        current_sort_by=sort_by,
        favorite_count=len(favorite_recipe_ids)
    )


@favorites_bp.route("/toggle/<int:recipe_id>", methods=["POST"])
@login_required
def toggle(recipe_id):
    """Toggle favorite status for a recipe"""
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Check if already favorited
    favorite = Favorite.query.filter_by(
        user_id=current_user.id,
        recipe_id=recipe_id
    ).first()

    if favorite:
        # Remove from favorites
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({
            'success': True,
            'favorited': False,
            'message': 'Recipe removed from favorites'
        })
    else:
        # Add to favorites
        new_favorite = Favorite(
            user_id=current_user.id,
            recipe_id=recipe_id
        )
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({
            'success': True,
            'favorited': True,
            'message': 'Recipe added to favorites'
        })


@favorites_bp.route("/check/<int:recipe_id>", methods=["GET"])
@login_required
def check(recipe_id):
    """Check if a recipe is favorited"""
    favorite = Favorite.query.filter_by(
        user_id=current_user.id,
        recipe_id=recipe_id
    ).first()
    
    return jsonify({
        'favorited': favorite is not None
    })
