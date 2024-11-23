from flask import Blueprint, render_template

import models

main_page = Blueprint('main_page',  __name__, template_folder='templates/main_page')


@main_page.route('/')
@main_page.route('/index')
def index():
    with models.Session() as session:
        session.commit()
    trip_level1 = session.get(models.Trip_type, 1)
    trip_level2 = session.query(models.Trip_level).filter(models.Trip_level.level_name == 'Начинающий')
    return render_template('index.html', title='Главная', trip_level1=trip_level1, trip_level2=trip_level2)