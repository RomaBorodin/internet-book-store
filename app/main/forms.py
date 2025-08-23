from flask_wtf import FlaskForm
from wtforms import TextAreaField, RadioField
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
    rating = RadioField(label='Оценка', choices=[(str(i), str(i)) for i in range(5, 0, -1)], validators=[DataRequired()])
    comment = TextAreaField(label='Комментарий', validators=[DataRequired('Оставьте сообщение')])
