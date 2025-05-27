from flask import Flask
from flask_login import LoginManager

from .auth import models
from config import settings
from .database import init_db
from .database import session_scope

from .auth import auth_bp


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = settings.SECRET_KEY

    init_db()

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        with session_scope() as session:
            user = session.query(models.User).get(user_id)
            if user:
                session.expunge(user)

            return user

    app.register_blueprint(auth_bp)

    return app
