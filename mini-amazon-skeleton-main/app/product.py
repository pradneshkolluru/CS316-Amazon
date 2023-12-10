import random
from flask import render_template,request
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.review import Review

from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter

bp = Blueprint('products', __name__)


# @bp.route('/products', methods = ['POST', 'GET'])
# def products():

#     topK = request.form.get('fname')

#     if topK == None or topK == '':
#         topK = -1
#     else:
#         topK = int(topK)
#     # get all available products for sale:
#     products = Product.get_all(True, topK)
#     # find the products current user has bought:
#     if current_user.is_authenticated:
#         purchases = Purchase.get_all_by_uid_since(
#             current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
#     else:
#         purchases = None
#     # render the page by adding information to the index.html file
#     return render_template('products.html',
#                            avail_products=products,
#                            purchase_history=purchases)


@bp.route('/products', methods = ['POST', 'GET'])
def products():

    stringMatch = request.form.get('stringMatch')
    catOpt = request.form.get('options')
    sortOpt = request.form.get('priceSort')

    print(sortOpt)

    search = False
    q = request.args.get('q')
    if q:
        search = True

    # get all available products for sale:
    products = Product.get_filtered2(True, strMatch = stringMatch, catMatch = catOpt, priceSort = sortOpt)

    page = request.args.get(get_page_parameter(), type=int, default=1)

    per_page = 12
    offset = (page - 1) * per_page

    sliced_products = products[offset: offset + per_page]

    pagination = Pagination(page=page, per_page = per_page, offset = offset, total= len(products), search=search, record_name='Products')

    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file

    # for i in sliced_products:

    #     i.avgRating = round(i.avgRating, 2)
        
    return render_template('products.html',
                           avail_products=sliced_products,
                           purchase_history=purchases,
                           pagination=pagination)


@bp.route('/products/<id>', methods = ['POST', 'GET'])
def product_info(id):
    # pagination stuff
    reviews = Review.get_all_by_pid(pid=id)

    page = request.args.get(get_page_parameter(), type=int, default=1)

    per_page = 4
    offset = (page - 1) * per_page

    sliced_reviews = reviews[offset: offset + per_page]

    pagination = Pagination(page=page, per_page = per_page, offset = offset, total= len(reviews), record_name='Products')

    # get specified product:

    product = Product.get_product_info(id)
    review = Review.get_all_by_pid(id)
    relatedProducts = Product.getProductsFromOtherVenders(id)
    numReviews = Product.getTotalNumProdReviews(id)


    # render the page by adding information to the products_indiv.html file
    return render_template('product_info.html',
                           product_info = product,
                           numReviews = numReviews, 
                           review_info = sliced_reviews,
                           other_vendors = relatedProducts, pagination=pagination
                           )
@bp.route('/products/cat/<category>', methods = ['POST', 'GET'])
def cat_products(category):

    stringMatch = ""
    kMost = ""
    catOpt = category
    sortOpt = ""

    print(sortOpt)

    search = False
    q = request.args.get('q')
    if q:
        search = True

    # get all available products for sale:
    products = Product.get_filtered2(True, strMatch = stringMatch, k = kMost, catMatch = catOpt, priceSort = sortOpt)

    page = request.args.get(get_page_parameter(), type=int, default=1)

    per_page = 12
    offset = (page - 1) * per_page

    sliced_products = products[offset: offset + per_page]

    pagination = Pagination(page=page, per_page = per_page, offset = offset, total= len(products), search=search, record_name='Products')

    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file

    # for i in sliced_products:

    #     i.avgRating = round(i.avgRating, 2)
        
    return render_template('products.html',
                           avail_products=sliced_products,
                           purchase_history=purchases,
                           pagination=pagination)

@bp.route('/', methods = ['POST'])
def random_products():
    stringMatch = ""
    kMost = ""
    catOpt = ""
    sortOpt = ""
    
    
    products = Product.get_filtered2(True, strMatch = stringMatch, k = kMost, catMatch = catOpt, priceSort = sortOpt)

    random.shuffle(products)

    selected_items = products[0:4]
        
    return render_template('index.html',
                           avail_products=selected_items)