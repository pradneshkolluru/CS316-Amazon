from flask import render_template
from flask_login import current_user
from flask import jsonify
from flask import redirect, url_for
import datetime

from .models.saveForLater import SaveForLater
from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('saveForLater', __name__)



@bp.route('/saveForLater/add/<int:product_id>', methods=['POST'])
def save_for_later(product_id):
    Cart.delete_item_from_cart(current_user.id, product_id)
    SaveForLater.add_item_to_saved(current_user.id, product_id)
    return redirect(url_for('cart.cart'))

@bp.route('/saveForLater/addToCart/<int:product_id>', methods=['POST'])
def add_saved_to_cart(product_id):
    SaveForLater.delete_from_saved(current_user.id, product_id)
    Cart.update_item_qty(current_user.id, product_id, 1)
    return redirect(url_for('cart.cart'))

@bp.route('/saveForLater/delete/<int:product_id>', methods=['POST'])
def delete_from_saved(product_id):
    SaveForLater.delete_from_saved(current_user.id, product_id)
    return redirect(url_for('cart.cart'))