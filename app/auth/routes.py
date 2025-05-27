from flask import flash, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

from app.extensions import db
from . import models
from . import forms
from . import auth_bp


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()

    if form.validate_on_submit():
        existing_user = models.User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Пользователь с такой почтой уже существует', 'danger')
            return redirect(url_for('auth.register'))

        new_user = models.User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    elif form.errors:
        flash(form.errors, 'danger')

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()

    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('auth.home'))

        flash('Не удалось войти', category='danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
