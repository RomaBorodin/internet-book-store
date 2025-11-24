from flask_wtf import FlaskForm
from wtforms import TextAreaField, RadioField, SubmitField
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
    rating = RadioField('Оценка', choices=[(str(i), str(i)) for i in range(5, 0, -1)], validators=[DataRequired()])
    comment = TextAreaField('Комментарий', validators=[DataRequired('Оставьте сообщение')])

    submit = SubmitField('Отправить отзыв')
