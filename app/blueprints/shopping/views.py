from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.shopping_list import ShoppingListItem
from app.blueprints.shopping.forms import ShoppingListItemForm


shopping_bp = Blueprint("shopping", __name__, url_prefix="/shopping")


@shopping_bp.route("/", methods=["GET"])
@login_required
def index():
    """Display the shopping list"""
    form = ShoppingListItemForm()
    
    # Get items grouped by category
    items = (
        ShoppingListItem.query
        .filter_by(user_id=current_user.id)
        .order_by(ShoppingListItem.checked.asc(), ShoppingListItem.category.asc(), ShoppingListItem.created_at.desc())
        .all()
    )
    
    # Group items by category
    categories = {}
    for item in items:
        cat = item.category or "other"
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
    
    # Count stats
    total_items = len(items)
    checked_items = sum(1 for item in items if item.checked)
    unchecked_items = total_items - checked_items
    
    return render_template(
        "shopping/index.html",
        form=form,
        items=items,
        categories=categories,
        total_items=total_items,
        checked_items=checked_items,
        unchecked_items=unchecked_items,
    )


@shopping_bp.route("/add", methods=["POST"])
@login_required
def add_item():
    """Add a new item to the shopping list"""
    form = ShoppingListItemForm()
    
    if form.validate_on_submit():
        item = ShoppingListItem(
            user_id=current_user.id,
            name=form.name.data,
            quantity=form.quantity.data,
            category=form.category.data,
            notes=form.notes.data,
        )
        db.session.add(item)
        db.session.commit()
        flash(f"Added '{item.name}' to your shopping list", "success")
    else:
        flash("Error adding item. Please check your input.", "error")
    
    return redirect(url_for("shopping.index"))


@shopping_bp.route("/toggle/<int:item_id>", methods=["POST"])
@login_required
def toggle_item(item_id):
    """Toggle the checked status of an item"""
    item = ShoppingListItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    item.checked = not item.checked
    db.session.commit()
    
    if request.is_json:
        return jsonify({"success": True, "checked": item.checked})
    
    return redirect(url_for("shopping.index"))


@shopping_bp.route("/delete/<int:item_id>", methods=["POST"])
@login_required
def delete_item(item_id):
    """Delete an item from the shopping list"""
    item = ShoppingListItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    item_name = item.name
    db.session.delete(item)
    db.session.commit()
    
    if request.is_json:
        return jsonify({"success": True})
    
    flash(f"Removed '{item_name}' from your shopping list", "info")
    return redirect(url_for("shopping.index"))


@shopping_bp.route("/clear-checked", methods=["POST"])
@login_required
def clear_checked():
    """Remove all checked items"""
    deleted_count = (
        ShoppingListItem.query
        .filter_by(user_id=current_user.id, checked=True)
        .delete()
    )
    db.session.commit()
    
    if request.is_json:
        return jsonify({"success": True, "deleted_count": deleted_count})
    
    flash(f"Removed {deleted_count} checked item(s)", "success")
    return redirect(url_for("shopping.index"))


@shopping_bp.route("/edit/<int:item_id>", methods=["GET", "POST"])
@login_required
def edit_item(item_id):
    """Edit an existing item"""
    item = ShoppingListItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    form = ShoppingListItemForm(obj=item)
    
    if form.validate_on_submit():
        item.name = form.name.data
        item.quantity = form.quantity.data
        item.category = form.category.data
        item.notes = form.notes.data
        db.session.commit()
        flash(f"Updated '{item.name}'", "success")
        return redirect(url_for("shopping.index"))
    
    return render_template("shopping/edit.html", form=form, item=item)


@shopping_bp.route("/add-from-recipe/<int:recipe_id>", methods=["POST"])
@login_required
def add_from_recipe(recipe_id):
    """Add all ingredients from a recipe to the shopping list"""
    from app.models.recipe import Recipe
    
    try:
        recipe = Recipe.query.get_or_404(recipe_id)
        
        if not recipe.ingredients:
            return jsonify({"success": False, "message": "No ingredients found in this recipe"}), 400
        
        added_count = 0
        for ingredient in recipe.ingredients:
            # Format quantity with unit
            quantity_str = ""
            if ingredient.quantity:
                quantity_str = f"{ingredient.quantity}"
                if ingredient.unit:
                    quantity_str += f" {ingredient.unit}"
            elif ingredient.unit:
                quantity_str = ingredient.unit
            
            # Check if item already exists
            existing_item = ShoppingListItem.query.filter_by(
                user_id=current_user.id,
                name=ingredient.name,
                checked=False  # Only check unchecked items
            ).first()
            
            if existing_item:
                # Update quantity if it exists
                if quantity_str and existing_item.quantity:
                    existing_item.notes = f"From recipe: {recipe.name}"
                continue
            
            # Create new shopping list item
            item = ShoppingListItem(
                user_id=current_user.id,
                name=ingredient.name,
                quantity=quantity_str or "As needed",
                category="groceries",  # Default category, could be improved
                notes=f"From recipe: {recipe.name}"
            )
            db.session.add(item)
            added_count += 1
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "added_count": added_count,
            "message": f"Added {added_count} ingredient(s) to your shopping list"
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error adding recipe to shopping list: {str(e)}")
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500
