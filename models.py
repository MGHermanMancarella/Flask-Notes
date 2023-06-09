from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    username = db.Column(
        db.Text,
        primary_key=True,
        nullable=False,
        unique=True)

    password = db.Column(
        db.String(100),
        nullable=False)

    email = db.Column(
        db.String(50),
        nullable=False
    )

    first_name = db.Column(
        db.String(30),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    # start_register
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        # return instance of user w/username and hashed password
        return cls(username=username, password=hashed, email=email, first_name=first_name, last_name=last_name)

    # end_register

    # start_authenticate
    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = cls.query.filter_by(username=username).one_or_none()
#one_or_none() is a filter_by method that returns one instance, none, or an error if two things meeting the validation are in the DB
# cls.query... is equivalent to User.query... because cls is passes as an argument, we use cls.
        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u
        else:
            return False
    # end_authenticate


class Note(db.Model):
    """class for notes."""

    __tablename__ = "notes"

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    owner_username = db.Column(
        db.String,
        db.ForeignKey('users.username'),
        nullable = False
    )

