from flask import Flask
from flask import render_template, flash, redirect, url_for, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# для хлебных крошек начало
from flask_breadcrumbs import Breadcrumbs, register_breadcrumb
from flask_menu import Menu
# from database import init_db
import models
# from models import Trip, Trip_type, Trip_level, Trip_description, Trip_duration, Photo, Trip_photo, Session, User
from sqlalchemy import select
from forms import LoginForm, RegistrationForm, CommentForm, FilterForm
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, current_user, login_user, logout_user

# для хлебных крошек конец


app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    with models.Session() as session:
        session.commit()
        return session.query(models.User).get(int(user_id))


# login_manager.login_view = 'login_manager'
# Session = sessionmaker(bind=engine)
# session = Session()


# для хлебных крошек начало
# menu = Menu()
# breadcrumbs = Breadcrumbs(init_menu=False)
#
# menu.init_app(app)
# breadcrumbs.init_app(app)
#
# Breadcrumbs(app=app)

# для хлебных крошек конец
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print(f"Вход выполнен: {current_user}")
        return redirect(url_for('index'))
    form = LoginForm()
    with models.Session() as session:
        session.commit()
    if form.validate_on_submit():
        user = session.scalar(
            select(models.User).where(models.User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Неверный логин или пароль')
            return redirect(url_for('login'))
        # print(f"user: {user.username}, {current_user}")
        login_user(user, remember=form.remember_me.data)
        # print(f"user: {user.about_me}")
        return redirect(url_for('index'))
    return render_template('login.html', title='Войти', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = models.User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        with models.Session() as session:
            session.add(user)
            session.commit()
        flash('Поздравляем! Вы зарегистрированы!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Зарегистрироваться', form=form)

@app.route('/')
@app.route('/index')
# @register_breadcrumb(app, '.', 'Главная')
def index():
    with models.Session() as session:
        session.commit()
    trip_level1 = session.get(models.Trip_type, 1)
    trip_level2 = session.query(models.Trip_level).filter(models.Trip_level.level_name == 'Начинающий')
    return render_template('index.html', title='Главная', trip_level1=trip_level1, trip_level2=trip_level2)

@app.route('/content/<type_name>/', defaults={'duration': "---", 'level': "---"}, methods=['GET', 'POST'])
@app.route('/content/<type_name>/<duration>/', defaults={'level': "---"}, methods=['GET', 'POST'])
@app.route('/content/<type_name>/<duration>/<level>', methods=['GET', 'POST'])
# @app.route('/content/<type_name>')
# @register_breadcrumb(app, './content/<type_name>', '<type_name>')
def content(type_name: str, duration: str, level: str):
# def content(type_name: str):
#     form = FilterForm()

    if duration == "---":
        form = FilterForm(duration=duration, level=level)
    else:
        form = FilterForm(duration=f"{duration[0]} день" if duration[0] == "1" else f"{duration[0]} дня", level=level)
    # form = FilterForm()
    with models.Session() as session:
        session.commit()
    # print(f"type_name: {type_name}")
    type_id = session.query(models.Trip_type).filter(models.Trip_type.type_name == type_name).first()
    trip_list = session.query(models.Trip, models.Trip_type, models.Trip_level, models.Trip_description, models.Trip_duration, models.Photo).join(models.Trip_type).join(models.Trip_level).join(models.Trip_description).join(models.Trip_duration).join(models.Photo).filter(models.Trip.trip_type_id == type_id.id)
    if duration != "---":
        if level == "---":
            trip_list = trip_list.filter(models.Trip_duration.id == int(duration[0])).all()
        else:
            trip_list = trip_list.filter(models.Trip_duration.id == int(duration[0])).filter(
                models.Trip_level.level_name == level).all()

    else:
        if level != "---":
            trip_list = trip_list.filter(models.Trip_level.level_name == level).all()


    if form.validate_on_submit():
        if form.show_btn:
            return redirect(url_for('content', title=type_name, type_name=type_name, duration=form.duration.data, level=form.level.data, type_id=type_id, form=form))



    # for (trip, type, level, description, duration, photo) in trip_list:
    #     print(f"Document: {trip, type, level, description, duration}")
    # trip_list = session.query(Trip).filter(Trip.trip_type_id == s1.id)
    # len_trip_list
    return render_template('content.html', title=type_name, trip_list=trip_list, type_id=type_id, form=form)

@app.route('/trip/<int:trip_id>', methods=['GET', 'POST'])
# @register_breadcrumb(app, './content/<type_name>', '<type_name>')
def trip(trip_id: int):
    form = CommentForm()

    if form.validate_on_submit():
        if form.add_btn:
            if current_user.is_authenticated:
                with models.Session() as session:
                    session.add(models.Comment(description=form.comment.data, trip_id=trip_id, user_id=current_user.id))
                    session.commit()
            else:
                flash('Комментарии могут оставлять только зарегистрированные пользователи')
            return redirect(url_for('trip', trip_id=trip_id))
        if form.update_btn:
            l = request.form["action"]
            print(f"request.form['action']: {l}")
            # print(f"select from update_btn: {str(select)}") # just to see what select is
            return redirect(url_for('trip', trip_id=trip_id))



    with models.Session() as session:
        session.commit()
    # print(f"type_name: {type_name}")
    # trip = session.get(Trip, trip_id)
    # type_id = session.query(Trip_type).filter(Trip_type.type_name == trip.trip_type_id).first()
    trip_photos = session.query(models.Trip_photo, models.Photo).join(models.Photo).filter(models.Trip_photo.trip_id==trip_id).all()
    len_trip_photos = len(trip_photos)
    trip_description = session.query(models.Trip, models.Trip_type, models.Trip_level, models.Trip_description, models.Trip_duration, models.Photo).join(models.Trip_type).join(models.Trip_level).join(models.Trip_description).join(models.Trip_duration).join(models.Photo).filter(models.Trip.id == trip_id)
    trip_comments = session.query(models.Comment, models.User).join(models.User).filter(models.Comment.trip_id == trip_id).order_by(models.Comment.id.desc())
    return render_template('trip.html', title=trip_description[0][1].type_name, trip_description=trip_description, trip_photos=trip_photos, len_trip_photos=len_trip_photos, form=form, trip_comments=trip_comments)

@app.route('/faq')
# @register_breadcrumb(app, './faq', 'FAQ')
def faq():
    return render_template('faq.html', title='FAQ')


if __name__ == '__main__':

    app.run(debug=True)

    # engine = create_engine('sqlite:////tmp/test.db', echo=True)
    # engine = create_engine("sqlite:///foo.db", echo=True)
    # Base.metadata.create_all(bind=engine)
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # tr_level = Trip_level('begginer')
    # session.add(tr_level)
    # session.commit()
    # import models
    # init_db()
