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
    # get all available products for sale:
    # products = Product.get_all(True)
    
    # find the items on the current user's wishlist:
    if current_user.is_authenticated:
        wishlist_items = WishlistItem.get_all_by_uid_since(current_user.id, 
                                                       datetime.datetime(1980, 9, 14, 0, 0, 0))
        return jsonify([item.__dict__ for item in wishlist_items])
    else:
        wishlist_items = None
        return jsonify({}), 404
    
    

