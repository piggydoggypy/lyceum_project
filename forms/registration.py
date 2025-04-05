from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import DataRequired


class registerForm(FlaskForm):
    login = StringField( validators=[DataRequired()])
    password = PasswordField( validators=[DataRequired()])
    name = StringField(validators=[DataRequired()])
    description = TextAreaField(validators=[DataRequired()])
    telephone = StringField(validators=[DataRequired()])
    email = EmailField(validators=[DataRequired()])
    is_employer = BooleanField('Я являюсь работодателем')
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Зарегистрироваться')
