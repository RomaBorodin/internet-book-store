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
        existing_email = models.User.query.filter_by(email=form.email.data).first()
        existing_number = models.User.query.filter_by(number=form.number.data).first()

        if existing_email:
            form.email.errors.append('Пользователь с такой почтой уже существует')
            return render_template('auth/register.html', form=form)
        if existing_number:
            form.number.errors.append('Пользователь с таким номером уже существует')
            return render_template('auth/register.html', form=form)

        new_user = models.User(
            name=form.name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            number=form.number.data,
            password_hash=generate_password_hash(form.password.data)
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()

    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('auth.home'))
        else:
            form.password.errors.append('Неверный пароль')
            return render_template('auth/login.html', form=form)

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/')
@auth_bp.route('/index')
def home():
    return render_template('index.html')
