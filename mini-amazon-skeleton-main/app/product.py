from flask import render_template,request
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('products', __name__)


@bp.route('/products', methods = ['POST', 'GET'])
def products():

    topK = request.form.get('fname')

    if topK == None or topK == '':
        topK = -1
    else:
        topK = int(topK)
    # get all available products for sale:
    products = Product.get_all(True, topK)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('products.html',
                           avail_products=products,
                           purchase_history=purchases)
