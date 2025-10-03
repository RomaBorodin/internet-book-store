from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_required

from app.extensions import db
from . import main_bp
from .. import models
from . import forms


@main_bp.route('/')
def home():
    top_books = models.Book.query.order_by(models.Book.avg_rating.desc()).limit(3).all()
    return render_template('main/index.html', top_books=top_books)


@main_bp.route('/search')
def search():
    query = request.args.get('q', '').strip().lower()
    if not query:
        return jsonify([])

    books = models.Book.query.filter(models.Book.title.ilike(f'%{query}%')).limit(10).all()
    results = [{'id': b.id, 'title': b.title} for b in books]
    return jsonify(results)


@main_bp.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_info(book_id):
    form = forms.ReviewForm()
    book = models.Book.query.get_or_404(book_id)

    if current_user.is_authenticated:
        existing_review = models.Review.query.filter_by(book_id=book.id, user_id=current_user.id).first()

    if form.validate_on_submit():
        if existing_review:
            existing_review.rating = int(form.rating.data)
            existing_review.comment = form.comment.data
        else:
            review = models.Review(
                book_id=book.id,
                user_id=current_user.id,
                rating=int(form.rating.data),
                comment=form.comment.data
            )

            db.session.add(review)
        db.session.commit()

        return redirect(url_for('main.book_info', book_id=book.id))

    item = models.CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()

    return render_template('main/book_page.html', book=book, item=item, form=form)


@main_bp.route('/delete_review/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    review = models.Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('main.book_info', book_id=review.book_id))


@main_bp.route('/catalog')
def catalog():
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'default', type=str)
    genre = request.args.get('genre', 'all', type=str)

    query = models.Book.query

    genres = [g[0] for g in db.session.query(models.Book.genre).distinct().all()]
    if genre != 'all':
        query = query.filter(models.Book.genre == genre)

    match sort:
        case 'rating_desc':
            query = query.order_by(models.Book.avg_rating.desc())
        case 'rating_asc':
            query = query.order_by(models.Book.avg_rating.asc())
        case 'price_desc':
            query = query.order_by(models.Book.price.desc())
        case 'price_asc':
            query = query.order_by(models.Book.price.asc())
        case _:
            query = query.order_by(models.Book.id)

    books = query.paginate(page=page, per_page=3, error_out=False)

    return render_template('main/catalog.html', books=books, sort=sort, genre=genre, genres=genres)
