from flask_login import UserMixin
from app.extensions import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    number = db.Column(db.String(16), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
