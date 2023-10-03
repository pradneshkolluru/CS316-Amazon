from flask import render_template
from flask_login import current_user
from flask import jsonify
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.wishlist import WishlistItem

from flask import Blueprint
bp = Blueprint('wishlist', __name__)


@bp.route('/wishlist')
def wishlist():

    # find the products current user has bought:
    if current_user.is_authenticated:
        wishList = WishlistItem.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))

        print(wishList)
        return jsonify([wish.__dict__ for wish in wishList])
    else:
        return jsonify({}), 404
    # render the page by adding information to the index.html file
    
