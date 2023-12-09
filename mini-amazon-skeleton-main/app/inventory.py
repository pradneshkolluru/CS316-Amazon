from flask import render_template
from flask_login import current_user
from flask import jsonify
from flask import request
from flask import redirect, url_for

from .models.inventory import InventoryItem
from .models.user import User
from .models.product import Product


from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter

bp = Blueprint('inventory', __name__)

@bp.route('/inventory/<int:sid>')
def inventory(sid):
    # get products in inventory of one seller
    seller = User.is_seller(sid)
    items = InventoryItem.get_all_by_sid(sid)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    offset = (page - 1) * per_page
    sliced_items = items[offset: offset + per_page]
    pagination = Pagination(page=page, per_page = per_page, offset = offset, total= len(items), record_name='Entries')
    return render_template('inventory.html',
                           items=sliced_items,
                           items_length=len(items),
                           pagination=pagination, seller=seller)

@bp.route('/inventory/add', methods=['POST'])
def inventory_add():  
    if current_user.is_authenticated:
        pid_input = request.form.get('pid')
        product_name = request.form.get('product_name').lower()
        quantity_input = request.form.get('quantity')

        if quantity_input == "" or (pid_input == "" and product_name == ""): # invalid submission
            # flash error message!!
            return redirect(url_for('inventory.inventory', sid=current_user.id))
        if pid_input == "": # used product_name
            product_name = request.form.get('product_name').lower()
            quantity = int(request.form.get('quantity'))
            item = InventoryItem.update_inventory(current_user.id, quantity, product_name=product_name)
        elif product_name == "": # used pid
            pid = int(pid_input) 
            quantity = int(request.form.get('quantity'))
            item = InventoryItem.update_inventory(current_user.id, quantity, pid=pid)
    else:
        item = None
        return jsonify({}), 404
    return redirect(url_for('inventory.inventory', sid=current_user.id))

@bp.route('/inventory/delete/<int:product_id>', methods=['POST'])
def inventory_delete(product_id):
    if current_user.is_authenticated:
        #item = InventoryItem.delete_item(current_user.id, product_id)
        item = InventoryItem.update_quantity(current_user.id,product_id, 0)
    else:
        item = None
        return jsonify({}), 404
    return redirect(url_for('inventory.inventory', sid=current_user.id))

@bp.route('/inventory/update', methods=['POST'])
def inventory_update_quantity():
    if current_user.is_authenticated:
        pid = int(request.form.get('pid'))
        quantity = int(request.form.get('quantity'))
        item = InventoryItem.update_inventory(current_user.id, quantity, pid=pid)
    else:
        item = None
        return jsonify({}), 404
    return redirect(url_for('inventory.inventory', sid=current_user.id))

@bp.route('/inventory/newProduct', methods=['POST', 'GET'])
def add_new_product_route():


    name = request.form.get('product_name')
    print(name)
    description = request.form.get('description')
    category = request.form.get('category')
    price = request.form.get('price')
    quantity = request.form.get('quantity')


    pid = Product.addNewProduct(current_user.id, name, category, description, price, quantity)


    return redirect(url_for('inventory.inventory', sid=current_user.id))

    





