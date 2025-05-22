from flask import Flask

from config import settings
from db.database import init_db
from routes import main_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY
app.register_blueprint(blueprint=main_blueprint)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
