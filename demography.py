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
        # tr_level = Trip_level(name='hghjh')
        # session.add(tr_level)
        session.commit()
    trip_level1 = session.get(Trip_level, 3)
    trip_level2 = session.query(Trip_level).filter(Trip_level.name == 'hjh')
    return render_template('index.html', title='Главная', trip_level1=trip_level1, trip_level2=trip_level2)


@app.route('/content')
@register_breadcrumb(app, './content', 'Контент')
def content():
    with Session() as session:
        session.commit()
    trip_level2 = session.query(Trip_level).filter(Trip_level.name == 'hjh')
    return render_template('content.html', title='Список походов', trip_level2=trip_level2)


@app.route('/faq')
@register_breadcrumb(app, './faq', 'FAQ')
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
