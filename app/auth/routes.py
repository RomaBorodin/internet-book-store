from flask import redirect, url_for, render_template, session, abort
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

        session['pending_user'] = {
            'name': form.name.data,
            'last_name': form.last_name.data,
            'email': form.email.data,
            'number': form.number.data,
            'password_hash': generate_password_hash(form.password.data)
        }
        session['pending_action'] = 'register'
        session['confirmation_code'] = '1234'

        return redirect(url_for('auth.confirm'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session['pending_user_id'] = user.id
            session['pending_action'] = 'login'
            session['confirmation_code'] = '1234'
            return redirect(url_for('auth.confirm'))

        form.password.errors.append('Неверный пароль')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/confirm', methods=['GET', 'POST'])
def confirm():
    form = forms.ConfirmForm()

    action = session.get('pending_action')
    confirmation_code = session.get('confirmation_code')

    if not action:
        abort(404)

    if form.validate_on_submit():
        if confirmation_code == form.code.data:
            if action == 'register':
                user_data = session.pop('pending_user')

                user = models.User(**user_data)

                db.session.add(user)
                db.session.commit()
                login_user(user)

            elif action == 'login':
                user = models.User.query.get(session.pop('pending_user_id'))
                login_user(user)

            session.pop('pending_action')
            session.pop('confirmation_code')

            return redirect(url_for('auth.home'))

        else:
            form.code.errors.append('Неверный код')

    return render_template('auth/confirm.html', form=form)
