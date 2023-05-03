"""Forms for users and notes."""

from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, Email
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField(
        "Username",
        validators=[InputRequired()],
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()],
    )


class RegisterForm(FlaskForm):
    """User registration form."""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max=20)],
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )

    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)],
    )

    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(max=30)],
    )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(max=30)],
    )


class NoteAddForm(FlaskForm):
    """Form for adding notes."""

    title = StringField(
        "Title",
        validators=[InputRequired(), Length(max=100)],
    )

    content = TextAreaField(
        "Content",
        validators=[InputRequired()],
        render_kw={'class': 'form-control', 'rows': 10}
    )


class NoteEditForm(NoteAddForm):
    """Form for editing notes."""


class CsrfForm(FlaskForm):
    """For actions where we want CSRF protection, but don't need any fields.

    Currently used for our "delete" buttons, which make POST requests, and the
    logout button, which makes POST requests.
    """
