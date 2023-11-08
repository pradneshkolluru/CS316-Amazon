from flask import render_template, request
from flask_login import current_user
import datetime

from .models.purchase import Purchase

from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter
bp = Blueprint('purchases', __name__)


@bp.route('/purchases')
# def purchases():
#     # get all available products for sale:
#     # find the products current user has bought:
#     if current_user.is_authenticated:
#         purchases = Purchase.get_all(
#             current_user.id)
#     else:
#         purchases = None
#     # render the page by adding information to the index.html file
#     return render_template('purchases.html',
#                            purchase_history=purchases)

def purchases():
    if current_user.is_authenticated:
        purchases = Purchase.get_all(
            current_user.id)
    else:
        purchases = None

    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    offset = (page - 1) * per_page

    sliced_products = purchases[offset: offset + per_page]

    pagination = Pagination(page=page, per_page = per_page, offset = offset, total= len(purchases), search=search, record_name='Purchases')
    return render_template('purchases.html',
                            purchase_history=purchases,
                            pagination=pagination)    
