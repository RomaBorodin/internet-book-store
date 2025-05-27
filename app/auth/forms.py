from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField(
        label='Username', validators=[DataRequired(), Length(min=4, max=100)]
    )
    email = StringField(
        label='Email', validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        label='Password', validators=[DataRequired(), Length(min=8, max=36)]
    )
    confirm = PasswordField(
        label='Confirm Password', validators=[DataRequired(), EqualTo(fieldname='password')]
    )


class LoginForm(FlaskForm):
    email = StringField(
        label='Email', validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        label='Password', validators=[DataRequired(), Length(min=8, max=36)]
    )
