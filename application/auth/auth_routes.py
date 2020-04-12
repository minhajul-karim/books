"""Blueprint to authenticate users."""

from .. import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import (Blueprint, render_template, request, abort, redirect,
                   url_for, flash, session)


# Set up a blueprint
auth_bp = Blueprint("auth_bp", __name__,
                    template_folder="templates")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    """
    User sign-up.

    GET: Serve sign up page.
    POST: Register user and redirect to homepage.
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            abort(400)
        if not password:
            abort(400)

        # Check if username already registered
        username_exists = db.execute("SELECT id FROM users WHERE username = :username",
                                     {"username": username})
        if username_exists:
            flash("Username alreay exists!")
            return redirect(url_for('.signup'))

        try:
            db.execute("INSERT INTO users(username, password) VALUES(:username, :password)",
                       {"username": username,
                        "password": generate_password_hash(password)})
            db.commit()
            return redirect(url_for('main_bp.home'))
        except Exception:
            abort(500)

    return render_template("signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Login user.

    GET: Serve login page.
    POST: If password mathces, log user in.
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            abort(400)
        if not password:
            abort(400)

        # Fetch data from db for username provided
        user = db.execute("SELECT * FROM users WHERE username = :username",
                          {"username": username}).fetchone()
        if not user:
            flash("Invalid username/password!")
            return redirect(url_for('.login'))

        # Check password
        if check_password_hash(user["password"], password):
            session["username"] = username
            return redirect(url_for('main_bp.home'))

        flash("Invalid username/password!")
        return redirect(url_for('.login'))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    """Logout user."""
    session.clear()
    return redirect(url_for("main_bp.home"))
