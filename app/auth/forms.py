from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp


class RegistrationForm(FlaskForm):
    name = StringField(label='Имя', validators=[
        DataRequired(message='Введите имя'), Length(min=2, max=100, message='Минимум 2 символа')
    ])
    last_name = StringField(label='Фамилия', validators=[
        DataRequired('Введите фамилию'), Length(min=2, max=100, message='Минимум 2 символа')
    ])
    email = StringField(label='Почта', validators=[
        DataRequired('Введите почту'), Email(message='Некорректная почта')
    ])
    number = StringField(label='Номер телефона', validators=[
        DataRequired('Введите номер телефона'),
        Regexp(r'^\+?\d{6,16}$', message='Телефон должен состоять из цифр (минимум 6) и знака в начале')
    ])
    password = PasswordField(label='Пароль', validators=[
        DataRequired('Введите пароль'), Length(min=8, max=36, message='Пароль должен быль от 8 до 36 символов')
    ])
    confirm = PasswordField(label='Подтвердить пароль', validators=[
        DataRequired('Введите пароль еще раз'), EqualTo(fieldname='password', message='Пароли не совпадают')
    ])


class LoginForm(FlaskForm):
    email = StringField(label='Почта', validators=[
        DataRequired('Введите почту'), Email(message='Некорректная почта')
    ])
    password = PasswordField(label='Пароль', validators=[
        DataRequired('Введите пароль'), Length(min=8, max=36, message='Пароль должен быль от 8 до 36 символов')
    ])


class ConfirmForm(FlaskForm):
    code = PasswordField(label='Код для входа: 1234', validators=[
        DataRequired('Введите код'), Length(max=4)
    ])
