from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length


# from content_pages.content_pages import session # most likely due to a circular import
# import content_pages.content_pages as content_pages # most likely due to a circular import
# session = db_session.create_session()
# def get_durations_list():
#   # global session
#   durations = content_pages.session.query(models.Trip_duration).all()
#   durations_list = ["---"] + [f"{i.duration} день" if i.id == 1 else f"{i.duration} дня" for i in durations]
#   return durations_list
#
# def get_levels_list():
#   # global session
#   # session = db_session.create_session()
#   levels = content_pages.session.query(models.Trip_level).all()
#   levels_list = ["---"] + [i.level_name for i in levels]
#   return levels_list

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

  # with models.Session() as session:
  #   durations = session.query(models.Trip_duration).all()
  #   durations_list = ["---"] + [f"{i.duration} день" if i.id == 1 else f"{i.duration} дня" for i in durations]
  #
  #   levels = session.query(models.Trip_level).all()
  #   levels_list = ["---"] + [i.level_name for i in levels]




  duration = SelectField(u'Длительность', choices=[])
  level = SelectField('Уровень подготовки', choices=[])


  show_btn = SubmitField('Показать')
