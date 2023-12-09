from flask import render_template
from flask import redirect, url_for
from flask import request
from flask_login import current_user
import datetime
from humanize import naturaldate

from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart
from .models.order import Order

from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter

bp = Blueprint('order', __name__)

def humanize_time(dt):
    return naturaldate(dt)

@bp.route('/order/<int:oid>')
def get_order(oid):
    # find all the products from all the current user's orders:
    if current_user.is_authenticated:
        order_info = Order.get_order_info(current_user.id, oid)
        purchases_in_order = Order.get_items_in_order(oid)

        search = False
        q = request.args.get('q')
        if q:
            search = True
        
        page = request.args.get(get_page_parameter(), type=int, default=1)

        per_page = 10
        offset = (page - 1) * per_page

        sliced_items = purchases_in_order[offset: offset + per_page]

        pagination = Pagination(page=page, per_page = per_page, offset = offset, total= len(purchases_in_order), search=search, record_name='Items')

    else:
        order_info = None
        purchases_in_order = None
        pagination = None

        
    
    # render the page by adding information to the order.html file
    return render_template('order.html',
                           order_info=order_info,
                           num_items_in_order=len(purchases_in_order),
                           purchases_in_order=sliced_items,
                           humanize_time=humanize_time,
                           pagination=pagination)

@bp.route('/order-seller/<int:sid>')
def seller_orders(sid):
    if current_user.is_authenticated:
        orders_list = Order.get_all_orders_for_seller(sid)
        if not orders_list:
            orders_list = []
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
        revenue = None,
        num_items = None,
        fulfillment = None,
        purchase_date = None
    return render_template('seller_orders.html',
                           oids_list = oids,
                           revenue = order_revenue,
                           num_items = order_num_items,
                           fulfillment = order_fulfillment,
                           purchase_date = order_purchase_date)

@bp.route('/order-seller/<int:sid>/<int:oid>')
def seller_order_details(sid, oid):
    if current_user.is_authenticated:
        purchase_items = Order.get_order_info_for_seller(sid, oid)

        buyer_info = Order.get_buyer_info_from_purchase(oid)[0]

        buyer_name = str(buyer_info[0]).capitalize() + " " + str(buyer_info[1]).capitalize()
        buyer_address = buyer_info[2]
        buyer_email = buyer_info[3]

    return render_template('seller_order_details.html',
                           purchase_items=purchase_items,
                           oid = oid,
                           name = buyer_name,
                           address = buyer_address,
                           email = buyer_email)

@bp.route('/order-seller/<int:sid>/<int:oid>/<int:pid>',methods=['POST'])
def change_purchase_fulfillment_status(sid, oid, pid):
    if current_user.is_authenticated:
        curr_status = str(request.form.get('fulfillment_status'))
        new_status = False
        if curr_status == "Fulfilled":
            new_status = True
        purchases = Order.update_purchase_fulfillment(oid, pid, new_status)
        # then trigger function to show change in status in buyer's view
        Order.check_and_update_order_fulfillment(oid)
    return redirect(url_for('order.seller_order_details', sid=sid, oid = oid))