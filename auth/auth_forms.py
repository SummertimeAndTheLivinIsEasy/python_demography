from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

import models
from data import db_session


class LoginForm(FlaskForm):

  class Meta:
    locales = ['ru-RU', 'ru']

    def get_translations(self, form):
      return super(FlaskForm.Meta, self).get_translations(form)

  email = StringField('Email', validators=[DataRequired()],render_kw={'style': 'width: 100%', "placeholder": "Введите email"})
  password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'style': 'width: 100%', "placeholder": "Введите пароль"})
  remember_me = BooleanField('Запомнить меня')
  submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):

  class Meta:
    locales = ['ru-RU', 'ru']

    def get_translations(self, form):
      return super(FlaskForm.Meta, self).get_translations(form)

  username = StringField('Никнейм', validators=[DataRequired()], render_kw={'style': 'width: 100%', "placeholder": "Введите никнейм"})
  email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'style': 'width: 100%', "placeholder": "Введите email"})
  password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'style': 'width: 100%', "placeholder": "Введите пароль"})
  password2 = PasswordField(
      'Пароль ещё раз', validators=[DataRequired(), EqualTo('password')], render_kw={'style': 'width: 100%', "placeholder": "Пароль ещё раз"})
  submit = SubmitField('Зарегистрироваться')

  def validate_username(self, username):

    # with models.Session() as session:
    #   user = session.query(models.User).filter(models.User.username == username.data).first()
    #   if user is not None:
    #     raise ValidationError('Данное имя уже используется. Пожалуйста введите другое.')

    session = db_session.create_session()

    user = session.query(models.User).filter(models.User.username == username.data).first()
    if user is not None:
      raise ValidationError('Данное имя уже используется. Пожалуйста введите другое.')

  def validate_email(self, email):
    # with models.Session() as session:
    #   user = session.query(models.User).filter(models.User.email == email.data).first()
    #   if user is not None:
    #     raise ValidationError('Пользователь с такой почтой уже зарегистрирован')

    session = db_session.create_session()
    user = session.query(models.User).filter(models.User.email == email.data).first()
    if user is not None:
      raise ValidationError('Пользователь с такой почтой уже зарегистрирован')