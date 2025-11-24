from flask_login import UserMixin

from app.extensions import db
from sqlalchemy import func, select
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    number = db.Column(db.String(16), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)

    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')
    cart_items = db.relationship('CartItem', back_populates='user', cascade='all, delete-orphan')
    orders = db.relationship('Order', back_populates='user', cascade='all, delete-orphan')


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    cover = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    reviews = db.relationship('Review', back_populates='book', cascade='all, delete-orphan')
    cart_items = db.relationship('CartItem', back_populates='book', cascade='all, delete-orphan')

    @hybrid_property
    def avg_rating(self):
        avg = db.session.query(func.avg(Review.rating)).filter(Review.book_id == self.id).scalar()
        return round(avg, 1) if avg else 0

    @avg_rating.expression
    def avg_rating(cls):
        return (
            select(func.coalesce(func.avg(Review.rating), 0))
            .where(Review.book_id == cls.id)
            .correlate_except(Review)
            .scalar_subquery()
        )


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    book = db.relationship('Book', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')


class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', back_populates='cart_items')
    book = db.relationship('Book', back_populates='cart_items')


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='Принят', nullable=False)
    number = db.Column(db.String(20), nullable=False)
    delivery_method = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    note = db.Column(db.Text)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)

    order_items = db.relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    user = db.relationship('User', back_populates='orders')


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    order = db.relationship('Order', back_populates='order_items')
    book = db.relationship('Book')
