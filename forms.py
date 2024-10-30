from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
  username = StringField('Email', validators=[DataRequired()],render_kw={'style': 'width: 100%', "placeholder": "Введите email"})
  password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'style': 'width: 100%', "placeholder": "Введите пароль"})
  remember_me = BooleanField('Запомнить меня')
  submit = SubmitField('Войти')