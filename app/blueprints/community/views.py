from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from app.extensions import db
from app.models.recipe import Recipe
from app.models.comment import Comment
from app.models.post import Post
from app.models.image import Image
from app.models.category import Category
from app.blueprints.community.forms import PostForm, CommentForm
from app.services.upload import upload_service


community_bp = Blueprint("community", __name__, url_prefix="/feed")


@community_bp.route("/", methods=["GET", "POST"])
@login_required
def feed():
    post_form = PostForm()
    comment_form = CommentForm()

    # Handle post creation
    if request.method == "POST" and "content" in request.form and "recipe_id" not in request.form:
        if post_form.validate_on_submit():
            try:
                # Create the post
                post = Post(
                    title=post_form.title.data if post_form.title.data else None,
                    content=post_form.content.data,
                    user_id=current_user.id,
                    status="published"
                )
                db.session.add(post)
                db.session.flush()  # Get the post ID
                
                # Handle image uploads
                uploaded_files = request.files.getlist('images')
                if uploaded_files:
                    for file_field in uploaded_files:
                        if file_field and file_field.filename:
                            try:
                                ok, url = upload_service.upload_file(file_field)
                                if ok and url:
                                    image = Image(url=url, post_id=post.id)
                                    db.session.add(image)
                            except Exception as e:
                                print(f"Error uploading image: {str(e)}")
                                continue
                
                db.session.commit()
                flash("Post created!", "success")
                return redirect(url_for("community.feed"))
            except Exception as e:
                db.session.rollback()
                flash(f"Error creating post: {str(e)}", "error")
        else:
            flash("Please fill in all required fields", "error")

    # Handle comment creation
    if request.method == "POST" and "recipe_id" in request.form:
        if comment_form.validate_on_submit():
            recipe_id = request.form.get("recipe_id")
            if recipe_id:
                try:
                    recipe_id = int(recipe_id)
                    c = Comment(content=comment_form.comment_text.data, user_id=current_user.id, recipe_id=recipe_id)
                    db.session.add(c)
                    db.session.commit()
                    flash("Comment posted", "success")
                except Exception as e:
                    db.session.rollback()
                    flash("Failed to post comment", "error")
            return redirect(url_for("community.feed"))

    recipes = (
        Recipe.query
        .options(
            joinedload(Recipe.images),
            joinedload(Recipe.comments).joinedload(Comment.author),
            joinedload(Recipe.author),
            joinedload(Recipe.category)
        )
        .filter(Recipe.public == True)
        .order_by(Recipe.created_at.desc())
        .limit(20)
        .all()
    )
    posts = (
        Post.query
        .options(joinedload(Post.images), joinedload(Post.author))
        .filter(Post.status == "published")
        .order_by(Post.created_at.desc())
        .limit(20)
        .all()
    )
    return render_template("community/feed.html", recipes=recipes, posts=posts, post_form=post_form, comment_form=comment_form)

