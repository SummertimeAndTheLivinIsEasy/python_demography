from flask import Flask
from flask import render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# для хлебных крошек начало
from flask_breadcrumbs import Breadcrumbs, register_breadcrumb
from flask_menu import Menu
# from database import init_db
from models import *
from sqlalchemy import select
# для хлебных крошек конец


app = Flask(__name__)

# Session = sessionmaker(bind=engine)
# session = Session()


# для хлебных крошек начало
menu = Menu()
breadcrumbs = Breadcrumbs(init_menu=False)

menu.init_app(app)
breadcrumbs.init_app(app)

Breadcrumbs(app=app)


# для хлебных крошек конец


@app.route('/')
@app.route('/index')
@register_breadcrumb(app, '.', 'Главная')
def index():
    with Session() as session:
        session.commit()
    trip_level1 = session.get(Trip_type, 1)
    trip_level2 = session.query(Trip_level).filter(Trip_level.level_name == 'Начинающий')
    return render_template('index.html', title='Главная', trip_level1=trip_level1, trip_level2=trip_level2)


@app.route('/content/<type_name>')
# @register_breadcrumb(app, './content/<type_name>', '<type_name>')
def content(type_name: str):
    with Session() as session:
        session.commit()
    # print(f"type_name: {type_name}")
    type_id = session.query(Trip_type).filter(Trip_type.type_name == type_name).first()
    trip_list = session.query(Trip, Trip_type, Trip_level, Trip_description, Trip_duration, Photo).join(Trip_type).join(Trip_level).join(Trip_description).join(Trip_duration).join(Photo).filter(Trip.trip_type_id == type_id.id)
    # for (trip, type, level, description, duration, photo) in trip_list:
    #     print(f"Document: {trip, type, level, description, duration}")
    # trip_list = session.query(Trip).filter(Trip.trip_type_id == s1.id)
    return render_template('content.html', title=type_name, trip_list=trip_list, type_id=type_id)

@app.route('/trip/<int:trip_id>')
# @register_breadcrumb(app, './content/<type_name>', '<type_name>')
def trip(trip_id: int):
    with Session() as session:
        session.commit()
    # print(f"type_name: {type_name}")
    # trip = session.get(Trip, trip_id)
    # type_id = session.query(Trip_type).filter(Trip_type.type_name == trip.trip_type_id).first()
    trip_photos = session.query(Trip_photo, Photo).join(Photo).filter(Trip_photo.trip_id==trip_id).all()
    len_trip_photos = len(trip_photos)
    trip_description = session.query(Trip, Trip_type, Trip_level, Trip_description, Trip_duration, Photo).join(Trip_type).join(Trip_level).join(Trip_description).join(Trip_duration).join(Photo).filter(Trip.id == trip_id)
    return render_template('trip.html', title=trip_description[0][1].type_name, trip_description=trip_description, trip_photos=trip_photos, len_trip_photos=len_trip_photos)

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
