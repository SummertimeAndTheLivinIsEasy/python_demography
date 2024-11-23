from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length

import models


class CommentForm(FlaskForm):
  class Meta:
    locales = ['ru-RU', 'ru']

    def get_translations(self, form):
      return super(FlaskForm.Meta, self).get_translations(form)


  comment = TextAreaField('Say something', validators=[DataRequired(), Length(min=10, max=1000)], render_kw={'style': 'width: 100%', "placeholder": "Введите комментарий"})
  add_btn = SubmitField('Добавить', render_kw={'style': 'width: 25%'})
  update_btn = SubmitField('Изменить', render_kw={'style': 'width: 20%'})
  delete_btn = SubmitField('Удалить', render_kw={'style': 'width: 20%'})


class FilterForm(FlaskForm):
  class Meta:
    locales = ['ru-RU', 'ru']

    def get_translations(self, form):
      return super(FlaskForm.Meta, self).get_translations(form)

  with models.Session() as session:
    durations = session.query(models.Trip_duration).all()
    durations_list = ["---"] + [f"{i.duration} день" if i.id == 1 else f"{i.duration} дня" for i in durations]

    levels = session.query(models.Trip_level).all()
    levels_list = ["---"] + [i.level_name for i in levels]


  duration = SelectField(u'Длительность', choices=durations_list)
  level = SelectField('Уровень подготовки', choices=levels_list)

  show_btn = SubmitField('Показать')
