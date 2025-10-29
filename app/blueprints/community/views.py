from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.recipe import Recipe
from app.models.comment import Comment
from app.models.post import Post
from app.blueprints.community.forms import PostForm


community_bp = Blueprint("community", __name__, url_prefix="/feed")


@community_bp.route("/", methods=["GET", "POST"])
@login_required
def feed():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("Post created!", "success")
        return redirect(url_for("community.feed"))

    # allow quick comment on a recipe
    if request.method == "POST":
        recipe_id = request.form.get("recipe_id")
        text = (request.form.get("comment") or "").strip()
        if recipe_id and text:
            try:
                recipe_id = int(recipe_id)
                c = Comment(comment_text=text, user_id=current_user.id, recipe_id=recipe_id)
                db.session.add(c)
                db.session.commit()
                flash("Comment posted", "success")
            except Exception:
                db.session.rollback()
                flash("Failed to post comment", "danger")
        return redirect(url_for("community.feed"))

    recipes = Recipe.query.filter(Recipe.public == True).order_by(Recipe.created_at.desc()).limit(20).all()
    posts = Post.query.order_by(Post.created_at.desc()).limit(20).all()
    return render_template("community/feed.html", recipes=recipes, posts=posts, form=form)

