from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user

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

    return render_template('main/book_page.html', book=book, form=form)


@main_bp.route('/delete_review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    review = models.Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('main.book_info', book_id=review.book_id))
