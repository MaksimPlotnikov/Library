from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
    title = StringField('Название Книги', validators=[DataRequired()])
    content = TextAreaField("Отзыв")
    submit = SubmitField('Применить')