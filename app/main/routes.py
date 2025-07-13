from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user

from . import main_bp
from .. import models


@main_bp.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('main/home.html')
    else:
        return render_template('main/index.html')


@main_bp.route('/search')
def search():
    query = request.args.get('q', '').strip().lower()
    if not query:
        return jsonify([])

    books = models.Book.query.filter(models.Book.title.ilike(f'%{query}%')).limit(10).all()
    results = [{'id': b.id, 'title': b.title} for b in books]
    return jsonify(results)
