from flask import Blueprint, flash, redirect, url_for, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

from db.database import session_scope
import db.models

main_blueprint = Blueprint('main', __name__)


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


@main_blueprint.route('/')
@login_required
def home():
    return render_template('index.html', name=current_user.username)


@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        with session_scope() as session:
            user = session.query(db.models.User).filter_by(email=form.email.data).first()
        if user:
            flash('User with this email already exists', 'danger')
            return redirect(url_for('main.register', form=form))

        user = db.models.User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )

        with session_scope() as session:
            session.add(user)
        return redirect(url_for('main.login'))

    elif form.errors:
        flash(form.errors, 'danger')

    return render_template('register.html', form=form)


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        with session_scope() as session:
            user = session.query(db.models.User).filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                return redirect(url_for('main.home'))

        flash('Login failed', category='danger')

    return render_template('login.html', form=form)


@main_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))
