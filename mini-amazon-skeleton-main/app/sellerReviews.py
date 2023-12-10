from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user
from datetime import datetime


from .models.sellerReview import SellerReview

from flask import Blueprint
bp = Blueprint('sellerReviews', __name__)


@bp.route('/sellerReviews')
def sellerReviews():
    # get all reviews by user:   
    if current_user.is_authenticated:
        reviews = SellerReview.get_all(
            current_user.id)
        
        print(reviews)
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
@bp.route('/sellerReviews/add/<id>', methods=['POST', 'GET'])
def add_review(id):
    if SellerReview.review_exists(current_user.id, id):
        flash('You have already reviewed this product')
        return redirect(url_for('users.public_view', id=id))
    else:
        uid=current_user.id
        time_posted = datetime.now()
        rating = request.form.get("newRating")
        review_text = request.form.get("newReview")
        SellerReview.add_review(uid=uid, sid=id, time_posted=time_posted,rating=rating, review_text=review_text)
        return redirect(url_for('users.public_view', id=id))