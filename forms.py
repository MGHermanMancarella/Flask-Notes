from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email


class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField(
        "Username",
        validators=[InputRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )

    email = StringField(
        "Email",
        validators=[Email()]
    )

    first_name = StringField(
        "First Name",
        validators=[InputRequired()]
    )

    last_name = PasswordField(
        "Last Name",
        validators=[InputRequired()]
    )

class LoginForm(FlaskForm):
    """Form for registering a user."""

    username = StringField(
        "Username",
        validators=[InputRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )

class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""