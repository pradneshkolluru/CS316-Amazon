from flask import render_template
from flask import redirect, url_for
from flask import request
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('cart', __name__)


@bp.route('/cart')
def cart():
    # find the products current user has added to cart:
    if current_user.is_authenticated:
        cart_products = Cart.get_items_in_cart(current_user.id)
        total_cart_price = Cart.get_total_price(current_user.id)
    else:
        cart_products = None
        total_cart_price = 0
    # render the page by adding information to the cart.html file
    return render_template('cart.html',
                           cart_products=cart_products,
                           total_cart_price=total_cart_price)


@bp.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    Cart.update_item_qty(current_user.id, product_id, 1)
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