"""Flask app for dessert demo."""

import os
from flask import Flask, request, jsonify, redirect, session, render_template, flash
from models import db, connect_db, User
from forms import RegisterForm, LoginForm, CSRFProtectForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///flask_notes')
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.get("/")
def homepage():
    """Redirect to /register}"""

    form = CSRFProtectForm()

    return redirect("/register", form=form)


@app.route("/register", methods=["GET", "POST"])
def register_form():
    """Create form or validate form data and create user}"""

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(name, pwd, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        return redirect("/users/<username>")

    else:
        return render_template("register.html", form=form)


@app.get("/users/<username>")
def list_single_dessert(username):
    """Example hidden page for logged-in users only."""

    if "user_id" not in session:
        flash("You must be logged in to view!")
        return redirect("/login")

    else:
        user = User.query.get(username)
        return render_template("user.html", user=user)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, pwd)

        if user:
            session["user_id"] = user.id  # keep logged in
            return redirect("/users/<username>")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)
# end-login

@app.post("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        # Remove "user_id" if present, but no errors if it wasn't
        session.pop("user_id", None)

    return redirect("/")