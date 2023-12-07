from flask import render_template
from flask import redirect, url_for
from flask import request
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart
from .models.order import Order

from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter

bp = Blueprint('order', __name__)


@bp.route('/order/<int:oid>')
def orders(oid):
    # find all the products from all the current user's orders:
    if current_user.is_authenticated:
        purchases_in_order = Order.get_items_in_order(current_user.id, oid)
    else:
        purchases_in_order = None
        
    # search = False
    # q = request.args.get('q')
    # if q:
    #     search = True
    
    # page = request.args.get(get_page_parameter(), type=int, default=1)

    # per_page = 10
    # offset = (page - 1) * per_page

    # sliced_items = orders[offset: offset + per_page]

    # pagination = Pagination(page=page, per_page = per_page, offset = offset, total= len(orders), search=search, record_name='Items')

    # render the page by adding information to the order.html file
    return render_template('orders.html',
                           purchases_in_order=purchases_in_order)
                        #    orders_list=orders_list)
                        #    pagination=pagination)

@bp.route('/orders/seller')
def seller_orders():
    if current_user.is_authenticated:
        orders_list = Order.get_all_orders_for_seller(current_user.id)
    else:
        orders = None
    return render_template('seller_orders.html',
                           orders_list=orders_list)