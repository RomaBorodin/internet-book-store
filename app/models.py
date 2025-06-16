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

    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    cover = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    avg_rating = db.Column(db.Float, nullable=False, default=0.0)
    reviews_count = db.Column(db.Integer, nullable=False, default=0)

    reviews = db.relationship('Review', back_populates='book', cascade='all, delete-orphan')


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    book = db.relationship('Book', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')
