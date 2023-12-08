from curses import window
from flask import flash, render_template, request, redirect, url_for
from flask_login import current_user
from datetime import datetime
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
        newRating = request.form.get("newRating")
        Review.update_review(id=id, newInput=newReview, newInputRating=newRating)
        return redirect(url_for('reviews.reviews'))

# @bp.route('/updateRating/<id>', methods = ['POST', 'GET'])
# def update_rating(id):
#     if current_user.is_authenticated:
#         newRating = request.form.get("newRating")
#         Review.update_rating(id=id, newInput=newRating)
#         return redirect(url_for('reviews.reviews'))

@bp.route('/reviews/delete/<id>', methods=['POST'])
def delete_review(id):
    Review.delete_review(id=id)
    return redirect(url_for('reviews.reviews'))


@bp.route('/reviews/add/<id>', methods=['POST', 'GET'])
def add_review(id):
    if Review.review_exists(current_user.id, id):
        return "You have already reviewed this product"
    else:
        uid=current_user.id
        time_posted = datetime.now()
        rating = request.form.get("newRating")
        review_text = request.form.get("newReview")
        Review.add_review(uid=uid, pid=id, time_posted=time_posted,rating=rating, review_text=review_text)
        return redirect(url_for('reviews.reviews'))
