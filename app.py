from flask import Flask
from flask_login import LoginManager

import db.models
from config import settings
from db.database import init_db
from routes import main_blueprint, session_scope

app = Flask(__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY
app.register_blueprint(blueprint=main_blueprint)

login_manager = LoginManager(app)
login_manager.login_view = 'main.login'


@login_manager.user_loader
def load_user(user_id):
    with session_scope() as session:
        user = session.query(db.models.User).get(user_id)
        if user:
            session.expunge(user)

        return user


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
