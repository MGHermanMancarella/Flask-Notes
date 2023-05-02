"""Flask app for dessert demo."""

import os
from flask import Flask, request, jsonify, redirect
from models import db, connect_db, Dessert
from forms import RegisterForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///desserts')
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

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

        session["user_id"] = user.id
        return redirect("/users/<username>")

    else:
        return render_template("register.html", form=form)


@app.get("/users/<username>")
def list_single_dessert(dessert_id):
    """Return JSON {'dessert': {id, name, calories}}"""

    dessert = Dessert.query.get_or_404(dessert_id)
    serialized = dessert.serialize()

    return jsonify(dessert=serialized)


@app.post("/desserts")
def create_dessert():
    """Create dessert from posted JSON data & return it.

    Returns JSON {'dessert': {id, name, calories}}
    """

    name = request.json["name"]
    calories = request.json["calories"]

    new_dessert = Dessert(name=name, calories=calories)

    db.session.add(new_dessert)
    db.session.commit()

    serialized = new_dessert.serialize()

    # Return w/status code 201 --- return tuple (json, status)
    return (jsonify(dessert=serialized), 201)
