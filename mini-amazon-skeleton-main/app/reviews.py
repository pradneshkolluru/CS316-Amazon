from flask import render_template, request, redirect, url_for
from flask_login import current_user
import datetime

from .models.review import Review

from flask import Blueprint
bp = Blueprint('reviews', __name__)


@bp.route('/reviews')
def reviews():
    # get all reviews by user:   
    if current_user.is_authenticated:
        reviews = Review.get_all(
            current_user.id)
    else:
        reviews = None
    # render the page by adding information to the index.html file
    return render_template('reviews.html',
                           review_history=reviews)
@bp.route('/updateReview/<id>', methods = ['POST', 'GET'])
def update_review(id):
    if current_user.is_authenticated:
        newReview = request.form.get("newReview")
        Review.update_review(id=id, newInput=newReview)
        return redirect(url_for('reviews.reviews'))

@bp.route('/reviews/delete/<id>', methods=['POST'])
def delete_review(id):
    Review.delete_review(id=id)
    return redirect(url_for('reviews.reviews'))