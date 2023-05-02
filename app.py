"""Flask app for dessert demo."""

import os
from flask import Flask, redirect, session, render_template, flash
from models import db, connect_db, User
from forms import RegisterForm, LoginForm, CSRFProtectForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///flask_notes')
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'Flask-Post-Secret-Key'

connect_db(app)

SESSION_AUTH_KEY = "username"

@app.get("/")
def homepage():
    """Redirect to /register}"""

    return redirect("/register")


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

        session[SESSION_AUTH_KEY] = user.username #NOTE: Create a global var = "username" to prevent whoopsies
        return redirect(f"/users/{user.username}")

    else:
        return render_template("register.html", form=form)


@app.get("/users/<username>")
def display_user_data(username):
    """Shows logged in user data and does requisite checks"""

    if SESSION_AUTH_KEY not in session or session[SESSION_AUTH_KEY] != username:
        flash("You must be logged in to view!")
        return redirect("/login")

    else:
        form = CSRFProtectForm()
        user = User.query.get(username)
        return render_template("user.html", user=user, form=form)

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
            session[SESSION_AUTH_KEY] = user.username  # keep logged in
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)
# end-login

@app.post("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        # Remove "username" if present, but no errors if it wasn't
        session.pop(SESSION_AUTH_KEY, None)

    return redirect("/")