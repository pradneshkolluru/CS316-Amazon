from flask import render_template
from flask_login import current_user
import datetime

from .models.sellerReview import SellerReview

from flask import Blueprint
bp = Blueprint('sellerReviews', __name__)


@bp.route('/sellerReviews')
def sellerReviews():
    # get all reviews by user:   
    if current_user.is_authenticated:
        reviews = SellerReview.get_all(
            current_user.id)
    else:
        reviews = None
    # render the page by adding information to the index.html file
    return render_template('sellerReviews.html',
                           review_history=reviews)
