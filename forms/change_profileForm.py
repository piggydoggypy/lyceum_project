from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField, EmailField, TextAreaField, FileField
from wtforms.validators import DataRequired


class Change_profile(FlaskForm):
    name = StringField(validators=[DataRequired()])
    description = TextAreaField(validators=[DataRequired()])
    telephone = StringField(validators=[DataRequired()])
    file = FileField()
    submit = SubmitField('Сохранить изменения')
