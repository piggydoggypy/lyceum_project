from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import DataRequired


class NewVacancy(FlaskForm):
    title = StringField(validators=[DataRequired()])
    content = TextAreaField(validators=[DataRequired()])

    submit = SubmitField('Добавить вакансию')
