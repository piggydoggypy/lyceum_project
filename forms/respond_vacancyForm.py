from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField, EmailField, TextAreaField, FileField
from wtforms.validators import DataRequired


class respond_Form(FlaskForm):
    theme = StringField(validators=[DataRequired()])
    content = TextAreaField(validators=[DataRequired()])
    file = FileField()
    submit = SubmitField('Отправить')
