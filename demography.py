from flask import Flask
from flask_login import LoginManager


import models
from auth.auth import auth

from config import Config
from content_pages.content_pages import content_pages
from icons.icons import icons_bp
from main_page.main_page import main_page




app = Flask(__name__)
app.config.from_object(Config)

# app.register_blueprint(main_page, url_prefix='/main_page')
app.register_blueprint(main_page)
app.register_blueprint(auth)
app.register_blueprint(content_pages)
app.register_blueprint(icons_bp, url_prefix='/icons')

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    with models.Session() as session:
        session.commit()
        return session.query(models.User).get(int(user_id))



if __name__ == '__main__':
    app.run(debug=True)

