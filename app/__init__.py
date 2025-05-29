from flask import Flask

from config import settings
from .extensions import db, login_manager, migrate
from .auth import models, auth_bp


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = settings.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(user_id)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)

    return app
