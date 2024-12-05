from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user

from content_pages.content_forms import CommentForm
from content_pages.content_forms import FilterForm
import models
from data import db_session

content_pages = Blueprint('content_pages', __name__, template_folder='templates/content_pages', static_folder='static', static_url_path='/content_pages/static')

session = None
@content_pages.before_request
def before_request():
    global session
    session = db_session.create_session()

@content_pages.teardown_request
def teardown_request(request):
    global session
    session = None
    return request


@content_pages.route('/content/<type_name>/', defaults={'duration': "---", 'level': "---"}, methods=['GET', 'POST'])
@content_pages.route('/content/<type_name>/<duration>/', defaults={'level': "---"}, methods=['GET', 'POST'])
@content_pages.route('/content/<type_name>/<duration>/<level>', methods=['GET', 'POST'])
# @app.route('/content/<type_name>')
# @register_breadcrumb(app, './content/<type_name>', '<type_name>')
def content(type_name: str, duration: str, level: str):
    # print(duration)
    # print(level)
    form = FilterForm(duration=duration)

    # durations = session.query(models.Trip_duration).all()
    # durations_list = ["---"] + [f"{i.duration} день" if i.id == 1 else f"{i.duration} дня" for i in durations]
    # form.duration.choices = durations_list
    # print(form.duration)

    # levels = session.query(models.Trip_level).all()
    # levels_list = ["---"] + [i.level_name for i in levels]
    # form.level.choices = levels_list
    # print(form.level)
    #
    # print(duration)
    # print(level)

    if duration == "---":
        form = FilterForm(duration=duration, level=level)


    else:
        form = FilterForm(duration=f"{duration[0]} день" if duration[0] == "1" else f"{duration[0]} дня", level=level)
        # form.duration.data = f"{duration[0]} день" if duration[0] == "1" else f"{duration[0]} дня"
        # form.level.data = level
    # with models.Session() as session:
    #     session.commit()
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
            print(form.duration.data)
            print(form.level.data)
            return redirect(url_for('content_pages.content', title=type_name, type_name=type_name, duration=form.duration.data, level=form.level.data, type_id=type_id, form=form))
    return render_template('content.html', title=type_name, trip_list=trip_list,duration=form.duration.data, level=form.level.data, type_id=type_id, form=form)

@content_pages.route('/trip/<int:trip_id>', methods=['GET', 'POST'])
def trip(trip_id: int):
    form = CommentForm()

    if form.validate_on_submit():
        if form.add_btn:
            if current_user.is_authenticated:
                # with models.Session() as session:
                #     session.add(models.Comment(description=form.comment.data, trip_id=trip_id, user_id=current_user.id))
                #     session.commit()
                session.add(models.Comment(description=form.comment.data, trip_id=trip_id, user_id=current_user.id))
                session.commit()
            else:
                flash('Комментарии могут оставлять только зарегистрированные пользователи')
            return redirect(url_for('content_pages.trip', trip_id=trip_id))
        # if form.update_btn:
        #     l = request.form["action"]
        #     print(f"request.form['action']: {l}")
        #     # print(f"select from update_btn: {str(select)}") # just to see what select is
        #     return redirect(url_for('trip', trip_id=trip_id))



    # with models.Session() as session:
    #     session.commit()
    # print(f"type_name: {type_name}")
    # trip = session.get(Trip, trip_id)
    # type_id = session.query(Trip_type).filter(Trip_type.type_name == trip.trip_type_id).first()
    trip_photos = session.query(models.Trip_photo, models.Photo).join(models.Photo).filter(models.Trip_photo.trip_id==trip_id).all()
    len_trip_photos = len(trip_photos)
    trip_description = session.query(models.Trip, models.Trip_type, models.Trip_level, models.Trip_description, models.Trip_duration, models.Photo).join(models.Trip_type).join(models.Trip_level).join(models.Trip_description).join(models.Trip_duration).join(models.Photo).filter(models.Trip.id == trip_id)
    trip_comments = session.query(models.Comment, models.User).join(models.User).filter(models.Comment.trip_id == trip_id).order_by(models.Comment.id.desc())
    return render_template('trip.html', title=trip_description[0][1].type_name, trip_description=trip_description, trip_photos=trip_photos, len_trip_photos=len_trip_photos, form=form, trip_comments=trip_comments)

@content_pages.route('/comment_delete/<int:trip_id>/<int:comment_id>', methods=['GET', 'POST'])
def comment_del(trip_id: int, comment_id: int):
    # with models.Session() as session:
    #     comment = session.query(models.Comment).filter(models.Comment.id==comment_id and models.Comment.user_id==current_user.id).first()
    #     print("comment", comment)
    #     print("trip_id", trip_id)
    #     print("comment_id", comment_id)
    #     if comment:
    #         session.delete(comment)
    #         session.commit()
    #     return redirect(url_for('content_pages.trip', trip_id=trip_id))
    comment = session.query(models.Comment).filter(models.Comment.id==comment_id and models.Comment.user_id==current_user.id).first()
    if comment:
        session.delete(comment)
        session.commit()
    return redirect(url_for('content_pages.trip', trip_id=trip_id))

@content_pages.route('/faq')
def faq():
    return render_template('faq.html', title='FAQ')
