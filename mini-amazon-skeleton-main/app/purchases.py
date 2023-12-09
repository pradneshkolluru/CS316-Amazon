from flask import render_template, request
from flask_login import current_user
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import datetime
import base64
from io import BytesIO

from .models.purchase import Purchase
from .models.order import Order
from .models.product import Product

from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter
bp = Blueprint('purchases', __name__)


@bp.route('/purchases', methods = ['POST', 'GET'])
def purchases():
    if current_user.is_authenticated:
        years = Order.get_years(current_user.id)
        if not years:
            years = []
        all_purchases = Order.get_all_purchases_in_orders(current_user.id)
        
        query=[]
        stringMatch = request.form.get('stringMatch')
        if stringMatch:
            query.append(stringMatch)
        sellerMatch = request.form.get('sellerMatch')
        if sellerMatch:
            query.append(sellerMatch)
        year = request.form.get('years')
        if year:
            query.append(year)
        querystring=", ".join(query)
        
        all_purchases = Order.get_filtered(strMatch = stringMatch, uid=current_user.id, sellerMatch=sellerMatch, year=year)
    
        #Pagination
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
        if Order.amount_spent(current_user.id):
            dates, amounts = Order.amount_spent(current_user.id)
            fig = Figure(figsize=(9, 4))
            ax = fig.subplots()
            ax.plot(dates, amounts)
            ax.set_xlabel("Date of Purchase")
            ax.set_ylabel("Amount Spent")
            ax.scatter(dates, amounts)
            
            for (i, j) in zip(dates, amounts):
                ax.text(i, j, "$" + str(j), fontsize=8, ha='center', va="bottom")

            buf = BytesIO()
            fig.savefig(buf, format="png")
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
        else:
            data = None
        categories = []
        recommendations = []
        if Order.categories(current_user.id):
            categories = Order.categories(current_user.id)
            for category in categories:
                recommendations += Product.get_filtered2(True, strMatch = stringMatch, catMatch = category)
        if len(recommendations) >= 3:
            recommendations = recommendations[:3]
    else:
        # purchases = None
        #all_purchases = None
        pagination= None
    return render_template('purchases.html',
                            # purchase_history=purchases,
                            all_purchases=sliced_products,
                            pagination=pagination, years=years, query=querystring, 
                            data =data, categories=categories, recs = recommendations)    
