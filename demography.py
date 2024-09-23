from flask import Flask
from flask import render_template


# для хлебных крошек начало
from flask_breadcrumbs import Breadcrumbs, register_breadcrumb
from flask_menu import Menu
# для хлебных крошек конец


app = Flask(__name__)


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
    return render_template('index.html', title='Главная')


@app.route('/content')
@register_breadcrumb(app, './content', 'Контент')
def content():
    return render_template('content.html', title='Список походов')


@app.route('/faq')
@register_breadcrumb(app, './faq', 'FAQ')
def faq():
    return render_template('faq.html', title='FAQ')


if __name__ == '__main__':
    app.run(debug=True)

