from flask import flash, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from app.database import session_scope
from . import models
from . import forms
from . import auth_bp


@auth_bp.route('/')
@login_required
def home():
    return render_template('index.html', name=current_user.username) <- ошибка


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()

    if form.validate_on_submit():
        with session_scope() as session:
            user = session.query(models.User).filter_by(email=form.email.data).first()
        if user:
            flash('User with this email already exists', 'danger')
            return redirect(url_for('auth.register', form=form))

        user = models.User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )

        with session_scope() as session:
            session.add(user)
        return redirect(url_for('auth.login'))

    elif form.errors:
        flash(form.errors, 'danger')

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()

    if form.validate_on_submit():
        with session_scope() as session:
            user = session.query(models.User).filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                return redirect(url_for('auth.home'))

        flash('Login failed', category='danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
