from flask import render_template, redirect, url_for, request, jsonify

from . import main_bp
from .. import models


@main_bp.route('/')
def home():
    return render_template('main/index.html')


@main_bp.route('/search')
def search():
    query = request.args.get('q', '').strip().lower()
    if not query:
        return jsonify([])

    books = models.Book.query.filter(models.Book.title.ilike(f'%{query}%')).limit(10).all()
    results = [{'id': b.id, 'title': b.title} for b in books]
    return jsonify(results)
