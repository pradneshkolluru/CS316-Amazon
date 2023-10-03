from flask import render_template
from flask_login import current_user
import datetime
from flask import jsonify

from .models.wishlist import WishlistItem

from flask import Blueprint
bp = Blueprint('wishlist', __name__)

@bp.route('/wishlist')
def wishlist():
    # get wishlist items of one user
    if current_user.is_authenticated:
        date = datetime.datetime(1980, 9, 14, 0, 0, 0)
        items = WishlistItem.get_all_by_uid_since(current_user.id, date)
    else:
        items = None
        return jsonify({}), 404
    return jsonify([item.__dict__ for item in items])
