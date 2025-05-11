from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField, EmailField, TextAreaField, FileField
from wtforms.validators import DataRequired


class registerForm(FlaskForm):
    login = StringField( validators=[DataRequired()])
    password = PasswordField( validators=[DataRequired()])
    rep_password = PasswordField( validators=[DataRequired()])
    name = StringField(validators=[DataRequired()])
    description = TextAreaField(validators=[DataRequired()])
    telephone = StringField(validators=[DataRequired()])
    email = EmailField(validators=[DataRequired()])
    file = FileField()
    is_employer = BooleanField('Я являюсь работодателем')
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Зарегистрироваться')
