from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import DataRequired


class base_page(FlaskForm):
    search = EmailField()
    profile_btn = SubmitField('Мой профиль')
    logout_btn = SubmitField('Выйти из аккаунта')
    search_btn = SubmitField('Найти')
    login = SubmitField('Войти')
    registration = SubmitField('Зарегистрироваться')
