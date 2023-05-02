from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

class RegisterForm(FlaskForm):
    """Form for registering a user."""



    username = StringField(
        "Username",
        validators=[InputRequired()]

    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(),
                    Length(max=100, message="Password too long.")]
    )

    email = StringField(
        "Email",
        validators=[Email(), Length(max=50, message="Email too long.")]
    )

    first_name = StringField(
        "First Name",
        validators=[InputRequired(),
                    Length(max=30, message="First Name too long.")],
    )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired(),
                    Length(max=30, message="Last Name too long.")]
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