from flask import render_template, request
from flask_login import current_user
import datetime

from .models.purchase import Purchase
from .models.order import Order

from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter
bp = Blueprint('purchases', __name__)


@bp.route('/purchases', methods = ['POST', 'GET'])
def purchases():
    if current_user.is_authenticated:
        all_purchases = Order.get_all_purchases_in_orders(current_user.id)
        # purchases = Purchase.get_all(
        #     current_user.id)
        stringMatch = request.form.get('stringMatch')
        kMost = request.form.get('topK')
        sellerMatch = request.form.get('sellerMatch')
        print(sellerMatch)
        all_purchases = Order.get_filtered(strMatch = stringMatch, k = kMost, uid=current_user.id, sellerMatch=sellerMatch)
    else:
        # purchases = None
        all_purchases

    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    offset = (page - 1) * per_page

    # sliced_products = purchases[offset: offset + per_page]
    sliced_products = all_purchases[offset: offset + per_page]

    pagination = Pagination(page=page, per_page = per_page, offset = offset, total= len(all_purchases), search=search, record_name='Purchases')
    return render_template('purchases.html',
                            # purchase_history=purchases,
                            all_purchases=all_purchases,
                            pagination=pagination)    
