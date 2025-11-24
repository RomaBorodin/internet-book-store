from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, Regexp


class OrderForm(FlaskForm):
    number = StringField('Номер телефона', validators=[
        DataRequired('Введите номер телефона'),
        Regexp(r'^\+?\d{6,16}$', message='Телефон должен состоять из цифр (минимум 6) и знака в начале')
    ])
    delivery_method = RadioField('Способ доставки',
                                 choices=[('pickup', 'Самовывоз'), ('delivery', 'Доставка до двери')], default='pickup',
                                 validators=[DataRequired()])
    pickup_point = RadioField('Пункт самовывоза',
                              choices=[('point1', 'Точка 1'), ('point2', 'Точка 2'), ('point3', 'Точка 3')],
                              default='point1',
                              validators=[Optional()])
    address = StringField('Адрес доставки', validators=[Optional()])
    note = TextAreaField('Cообщение при доставке', validators=[Optional()])

    submit = SubmitField('Оформить заказ')
