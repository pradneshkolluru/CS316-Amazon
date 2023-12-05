from flask import redirect, render_template, request, url_for
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
@bp.route('/updateSellerReview/<id>', methods = ['POST', 'GET'])
def update_review(id):
    if current_user.is_authenticated:
        newReview = request.form.get("newReview")
        newRating = request.form.get("newRating")
        SellerReview.update_review(id=id, newInput=newReview, newInputRating=newRating)
        return redirect(url_for('sellerReviews.sellerReviews'))
@bp.route('/sellerReviews/delete/<id>', methods=['POST'])
def delete_review(id):
    SellerReview.delete_review(id=id)
    return redirect(url_for('sellerReviews.sellerReviews'))   