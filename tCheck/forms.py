from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, validators, SubmitField

class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    pin_code = StringField('Pin code', [validators.Length(min=4, max=6)])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25),validators.Optional()])
    pin_code = StringField('Pin code', [validators.Length(min=4, max=6)])
    submit = SubmitField('Submit')





