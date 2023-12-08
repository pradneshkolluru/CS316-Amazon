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

@bp.route('/order-seller/<int:sid>')
def seller_orders(sid):
    if current_user.is_authenticated:
        orders_list = Order.get_all_orders_for_seller(sid)
        oids = []
        # list of dictionaries with key: oid
        order_revenue = {}
        order_num_items = {}
        order_fulfillment = {}
        order_purchase_date = {} #default value
        for purchase in orders_list:
            oid = purchase[0]
            qty = purchase[2]
            unit_price = purchase[3]
            purchase_fulfilled = purchase[4]
            time_purchased = purchase[5]
            oids.append(oid)
            if oid in order_revenue:
                order_revenue[oid] += qty * unit_price
            if oid not in order_revenue:
                order_revenue[oid] = qty * unit_price
            if oid in order_num_items:
                order_num_items[oid] += qty
            if oid not in order_num_items:
                order_num_items[oid] = qty
            if oid in order_fulfillment:
                if order_fulfillment[oid]:
                    if not purchase_fulfilled:
                        order_fulfillment[oid] = "Not fulfilled"
            if oid not in order_fulfillment:
                if purchase_fulfilled:
                    order_fulfillment[oid] = "Fulfilled"
                else:
                    order_fulfillment[oid] = "Not fulfilled"
            if not oid in order_purchase_date:
                order_purchase_date[oid] = time_purchased
        
        oids = list(set(oids)) # only unique order ids

        # sort oids by time_purchased (reverse chronological order)
        oid_time = []
        for oid in oids:
            oid_time.append((oid, order_purchase_date[oid]))
        oid_time.sort(key = lambda x:x[1], reverse = True)
        oids = [o[0] for o in oid_time]

    else:
        oids_list = None
    # return render_template('seller_orders.html',
    #                        orders_list=orders_list)
    return render_template('seller_orders.html',
                           oids_list = oids,
                           revenue = order_revenue,
                           num_items = order_num_items,
                           fulfillment = order_fulfillment,
                           purchase_date = order_purchase_date)