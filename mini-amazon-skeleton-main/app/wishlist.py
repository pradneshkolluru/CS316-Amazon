from flask import render_template
from flask_login import current_user
import datetime

from .models.wishlist import Wishes
from flask import Blueprint

from flask import jsonify
from flask import redirect, url_for

bp = Blueprint('wishlist', __name__)

@bp.route('/wishlist')
def wishlist():
    if current_user.is_authenticated:
        wishes = Wishes.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        return jsonify([wish.__dict__ for wish in wishes])
    else:
       return jsonify({}), 404

@bp.route('/wishlist/add/<int:product_id>', methods=['POST'])
def add(product_id):
    if current_user.is_authenticated:
        Wishes.add_item(
            current_user.id, product_id
        )
    return redirect(url_for('wishlist.wishlist'))
    
