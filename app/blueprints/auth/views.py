from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user
from .forms import RegistrationForm, LoginForm
from app.repository.user import create_user, find_by_email

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        create_user(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data,
        )
        flash("Your account has been created! You are now able to log in", "success")
        return redirect(url_for("main.index"))
    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = find_by_email(form.email.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Invalid email or password.", "danger")
    return render_template("auth/login.html", form=form)
