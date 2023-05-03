"""Flask notes app."""

import os

from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User, Note
from forms import RegisterForm, LoginForm, NoteAddForm, NoteEditForm, CsrfForm

# key name used to store auth credentials in session
AUTH_KEY = "username"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///flask_notes")
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "i-have-a-secret"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.get("/")
def homepage():
    """Homepage of site; redirect to register."""

    return redirect("/register")


# ====================================================== Login/Register/Logout

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a user: produce form and handle form submission."""

    if AUTH_KEY in session:
        return redirect(f"/users/{session[AUTH_KEY]}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)

        db.session.commit()
        session[AUTH_KEY] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template("users/register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""

    if AUTH_KEY in session:
        return redirect(f"/users/{session[AUTH_KEY]}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)  # <User> or False
        if user:
            session[AUTH_KEY] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)


@app.post("/logout")
def logout():
    """Logout route."""

    form = CsrfForm()

    if form.validate_on_submit():
        session.pop(AUTH_KEY)
        return redirect("/login")

    else:
        # didn't pass CSRF; ignore logout attempt
        raise Unauthorized()


# ================================================================ User routes

@app.get("/users/<username>")
def show_user(username):
    """Show user & notes page for logged-in-users."""

    if AUTH_KEY not in session or username != session[AUTH_KEY]:
        raise Unauthorized()

    user = User.query.get_or_404(username)
    form = CsrfForm()

    return render_template("users/show.html", user=user, form=form)


@app.post("/users/<username>/delete")
def remove_user(username):
    """Remove user and redirect to login."""

    if AUTH_KEY not in session or username != session[AUTH_KEY]:
        raise Unauthorized()

    form = CsrfForm()

    if form.validate_on_submit():
        user = User.query.get_or_404(username)
        Note.query.filter_by(owner_username=username).delete()
        db.session.delete(user)
        db.session.commit()
        session.pop(AUTH_KEY)

        return redirect("/login")

    else:
        # didn't pass CSRF
        raise Unauthorized()


# =============================================================== Notes routes

@app.route("/users/<username>/notes/new", methods=["GET", "POST"])
def new_note(username):
    """Show add-note form and process it."""

    if AUTH_KEY not in session or username != session[AUTH_KEY]:
        raise Unauthorized()

    form = NoteAddForm()

    # make sure the user exists
    User.query.get_or_404(username)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(
            title=title,
            content=content,
            owner_username=username,
        )

        db.session.add(note)
        db.session.commit()

        return redirect(f"/users/{username}")

    else:
        return render_template("notes/new.html", form=form)


@app.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
def update_note(note_id):
    """Show update-note form and process it."""

    note = Note.query.get_or_404(note_id)

    if AUTH_KEY not in session or note.owner_username != session[AUTH_KEY]:
        raise Unauthorized()

    form = NoteEditForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{note.owner_username}")

    return render_template("/notes/edit.html", form=form, note=note)


@app.post("/notes/<int:note_id>/delete")
def delete_note(note_id):
    """Delete note."""

    note = Note.query.get_or_404(note_id)

    if AUTH_KEY not in session or note.owner_username != session[AUTH_KEY]:
        raise Unauthorized()

    form = CsrfForm()

    if form.validate_on_submit():   # <-- csrf checking!
        db.session.delete(note)
        db.session.commit()

        return redirect(f"/users/{note.owner_username}")

    else:
        # didn't pass CSRF
        raise Unauthorized()
