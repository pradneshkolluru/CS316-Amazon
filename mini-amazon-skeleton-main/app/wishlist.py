from flask import render_template
from flask_login import current_user
from flask import jsonify
from flask import redirect, url_for

import datetime
from humanize import naturaltime

from .models.wishlist import WishlistItem

from flask import Blueprint
bp = Blueprint('wishlist', __name__)

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

@bp.route('/wishlist')
def wishlist():
    # get wishlist items of one user
    if current_user.is_authenticated:
        date = datetime.datetime(1980, 9, 14, 0, 0, 0)
        items = WishlistItem.get_all_by_uid_since(current_user.id, date)
    else:
        items = None
        return jsonify({}), 404
    return render_template('wishlist.html',
                      items=items,
                      humanize_time=humanize_time)


@bp.route('/wishlist/add/<int:product_id>', methods=['POST'])
def wishlist_add(product_id):
    if current_user.is_authenticated:
        item = WishlistItem.add_item(current_user.id, product_id)
    else:
        item = None
        return jsonify({}), 404
    return redirect(url_for('wishlist.wishlist'))
