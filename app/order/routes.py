from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_required
from datetime import datetime

from app.extensions import db
from . import order_bp
from . import forms
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


@order_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    form = forms.OrderForm()
    cart_items = models.CartItem.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        return redirect(url_for('main.catalog'))

    if form.validate_on_submit():
        order = models.Order(
            user_id=current_user.id,
            date=datetime.now(),
            status='В обработке',
            number=form.number.data,
            delivery_method=form.delivery_method.data,
            address=form.address.data if form.delivery_method.data == 'delivery' else form.pickup_point.data,
            note=form.note.data,
            total_price=sum((item.book.price * item.quantity) for item in cart_items)
        )

        db.session.add(order)
        db.session.flush()

        for item in cart_items:
            order_item = models.OrderItem(
                order_id=order.id,
                book_id=item.book.id,
                quantity=item.quantity,
                price=item.book.price
            )

            db.session.add(order_item)

        models.CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()

        flash("Заказ успешно оформлен!", "success")

        return redirect(url_for('order.checkout'))  # тут должен быть редирект на историю заказов

    return render_template('order/checkout.html', form=form)
