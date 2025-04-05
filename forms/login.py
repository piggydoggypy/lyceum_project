from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
