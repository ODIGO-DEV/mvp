from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.user import User
from app.models.recipe import Recipe
from app.models.post import Post
from sqlalchemy import desc

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


@profile_bp.route("/")
@login_required
def index():
    """Display the user's profile page"""
    # Get user's statistics
    total_recipes = Recipe.query.filter_by(user_id=current_user.id).count()
    public_recipes = Recipe.query.filter_by(user_id=current_user.id, public=True).count()
    private_recipes = Recipe.query.filter_by(user_id=current_user.id, public=False).count()
    
    # Get user's recent recipes
    recent_recipes = Recipe.query.filter_by(user_id=current_user.id).order_by(desc(Recipe.created_at)).limit(6).all()
    
    # Get user's recent posts
    recent_posts = Post.query.filter_by(user_id=current_user.id).order_by(desc(Post.created_at)).limit(5).all()
    
    return render_template(
        "profile/index.html",
        user=current_user,
        total_recipes=total_recipes,
        public_recipes=public_recipes,
        private_recipes=private_recipes,
        recent_recipes=recent_recipes,
        recent_posts=recent_posts
    )


@profile_bp.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    """Edit user profile"""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        
        # Update user information
        current_user.name = name
        current_user.email = email
        current_user.phone = phone
        
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile.index"))
    
    return render_template("profile/edit.html", user=current_user)
