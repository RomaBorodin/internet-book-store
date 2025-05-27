from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField(
        label='Username', validators=[InputRequired(), Length(min=4, max=100)]
    )
    email = StringField(
        label='Email', validators=[InputRequired(), Email()]
    )
    password = PasswordField(
        label='Password', validators=[InputRequired(), Length(min=8, max=36)]
    )
    confirm_password = PasswordField(
        label='Confirm Password', validators=[InputRequired(), EqualTo(fieldname='password')]
    )


class LoginForm(FlaskForm):
    email = StringField(
        label='Email', validators=[InputRequired(), Email()]
    )
    password = PasswordField(
        label='Password', validators=[InputRequired(), Length(min=8, max=36)]
    )
