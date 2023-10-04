from flask import render_template
from flask_login import current_user
from flask import jsonify
from flask import redirect, url_for

from .models.inventory import InventoryItem

from flask import Blueprint
bp = Blueprint('inventory', __name__)

@bp.route('/inventory')
def inventory():
    # get products in inventory of one seller
    if current_user.is_authenticated:
        items = InventoryItem.get_all_by_sid(current_user.id)
    else:
        items = None
        return jsonify({}), 404
    return render_template('inventory.html',
                      items=items)

@bp.route('/inventory/add/<int:product_id>/<int:quantity>', methods=['POST'])
def inventory_add(product_id, quantity):
    if current_user.is_authenticated:
        item = InventoryItem.add_item(current_user.id, product_id, quantity)
    else:
        item = None
        return jsonify({}), 404
    return redirect(url_for('inventory.inventory'))