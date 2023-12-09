from flask import render_template
from flask import redirect, url_for, flash
from flask import request
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart
from .models.saveForLater import SaveForLater

from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter

bp = Blueprint('cart', __name__)


@bp.route('/cart')
def cart():
    # find the products current user has added to cart:
    if current_user.is_authenticated:
        cart_products = Cart.get_items_in_cart(current_user.id)
        total_cart_price = Cart.get_total_price(current_user.id)
        if total_cart_price == None:
            total_cart_price = 0
        num_line_items = len(cart_products)
        saved_items = SaveForLater.get_saved_items(current_user.id)

        search = False
        q = request.args.get('q')
        if q:
            search = True
        
        page = request.args.get(get_page_parameter(), type=int, default=1)

        per_page = 10
        offset = (page - 1) * per_page

        sliced_items = cart_products[offset: offset + per_page]

        pagination = Pagination(page=page, per_page = per_page, offset = offset, total= len(cart_products), search=search, record_name='Items')

    else:
        sliced_items = None
        total_cart_price = 0
        num_line_items = 0
        saved_items = None
        pagination = None
    
    
    # render the page by adding information to the cart.html file
    return render_template('cart.html',
                           cart_products=sliced_items,
                           total_cart_price=total_cart_price,
                           num_line_items=num_line_items,
                           saved_items=saved_items,
                           pagination=pagination)


@bp.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    Cart.update_item_qty(current_user.id, product_id, 1)
    return redirect(url_for('cart.cart'))

@bp.route('/cart/add_multiple/<int:product_id>', methods=['POST', 'GET'])
def add_multiple_to_cart(product_id):

    qty = request.form.get('addQuant')

    

    if qty:
        qty = int(qty)
    else:
        qty = 1

    print(qty)
    print("testing123")
    Cart.update_item_qty(current_user.id, product_id, qty)
    return redirect(url_for('cart.cart'))

@bp.route('/cart/delete/<int:product_id>', methods=['POST'])
def delete_from_cart(product_id):
    Cart.delete_item_from_cart(current_user.id, product_id)
    return redirect(url_for('cart.cart'))

@bp.route('/cart/update', methods=['POST'])
def change_item_qty():
    pid = int(request.form.get('pid'))
    qty = int(request.form.get('qty'))
    Cart.update_item_qty(current_user.id, pid, qty)
    return redirect(url_for('cart.cart'))

@bp.route('/cart/submit', methods=['POST'])
def try_submit_order():
    order_id = Cart.submit_cart(current_user.id)
    if order_id:
        flash("Order Submitted!")
        return redirect(url_for('order.get_order', oid = order_id))
    else:
        return redirect(url_for('cart.cart'))
    