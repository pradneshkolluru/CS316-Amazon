from flask import render_template
from flask_login import current_user
from flask import jsonify
from flask import redirect, url_for

from .models.inventory import InventoryItem

from flask import Blueprint
bp = Blueprint('Inventory', __name__)

@bp.route('/inventory')
def inventory():
    # get products in inventory of one seller
    if current_user.is_authenticated:
        items = InventoryItem.get_all_by_sid(current_user.id)
    else:
        items = None
        return jsonify({}), 404
    #return jsonify([item.__dict__ for item in items])
    return render_template('inventory.html',
                      items=items)