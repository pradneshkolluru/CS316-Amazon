from flask import render_template
from flask_login import current_user
import datetime

from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('purchases', __name__)


@bp.route('/purchases')
def purchases():
    # get all available products for sale:
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('purchases.html',
                           purchase_history=purchases)
