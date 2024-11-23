from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from sqlalchemy import select

import models
from auth.auth_forms import LoginForm, RegistrationForm



auth = Blueprint('auth', __name__, template_folder='templates/auth', static_folder='static')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print(f"Вход выполнен: {current_user}")
        return redirect(url_for('main_page.index'))
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
        return redirect(url_for("main_page.index"))
    return render_template('login.html', title='Войти', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_page.index'))

@auth.route('/register', methods=['GET', 'POST'])
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