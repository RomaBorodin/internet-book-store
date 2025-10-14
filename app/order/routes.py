from flask import render_template, redirect, request
from flask_login import current_user, login_required

from app.extensions import db
from . import order_bp
from .. import models


@order_bp.route('/cart')
@login_required
def cart():
    cart_items = models.CartItem.query.filter_by(user_id=current_user.id).order_by(models.CartItem.id).all()
    total = sum((item.book.price * item.quantity) for item in cart_items)

    return render_template('order/cart.html', cart_items=cart_items, total=total)


@order_bp.route('/cart_update/<int:book_id>', methods=['POST'])
@login_required
def cart_update(book_id):
    item = models.CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    action = request.form.get('action')

    if not item:
        item = models.CartItem(user_id=current_user.id, book_id=book_id, quantity=1)
        db.session.add(item)
    else:
        match action:
            case 'inc':
                item.quantity += 1
            case 'dec':
                if item.quantity == 1:
                    db.session.delete(item)
                else:
                    item.quantity -= 1
            case _:
                pass

    db.session.commit()

    next_url = request.form.get('next_url') or request.referrer
    return redirect(next_url)
