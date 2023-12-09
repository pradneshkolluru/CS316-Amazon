from flask import current_app as app
import io
import base64
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
matplotlib.use('Agg')


def adjust_brightness(img, factor):
    """Adjust the brightness of the image."""
    hsv = mcolors.rgb_to_hsv(img[:, :, :3])  # Convert RGB to HSV
    hsv[:, :, 2] *= factor  # Adjust the V channel (brightness)
    return mcolors.hsv_to_rgb(hsv)  # Convert back to RGB


def imagePic(name, pid):

    fig, ax = plt.subplots(figsize=(4, 4))

    bg_image = plt.imread('app/static/images/gargi.jpeg')

    bg_image = adjust_brightness(bg_image, 0.95)

    ax.imshow(bg_image, extent=[0, 1, 0, 1], zorder=-1)

    # background_color = np.random.rand(3,)  # Generating a random RGB color
    # plt.figure(figsize=(4, 4), facecolor=background_color)  # Set figure size and background color

    plt.text(0.5, 0.8, str(pid), fontsize=20, ha='center', color='black')
    plt.text(0.5, 0.9, str(name), fontsize=10, ha='center', color='black')

    plt.axis('off')

    buff = io.BytesIO()
    plt.savefig(buff, format='png')
    buff.seek(0)
    encodedPlot = base64.b64encode(buff.read()).decode('utf-8')


    return encodedPlot


class Product:
    def __init__(self, id, name, price, available, description, category, avgRating = 0):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.available = available
        self.avgRating = avgRating
        #self.image = imagePic(self.name, self.id)
        self.image = ""

    @staticmethod
    def get(id):

        query = '''
            SELECT id, name, price, available
            FROM Products
            WHERE id = :id
        '''
        rows = app.db.execute(query, id=id)
        return Product(*(rows[0])) if rows is not None else None
    
    @staticmethod
    def get_filtered(available=True, k=0, strMatch="", catMatch = "", priceSort = ""):

        print(catMatch)

        query = '''
            SELECT id, name, price, available, description, category
            FROM Products
            WHERE available = :available
        '''

        params = {"available": available}

        if strMatch:
            query += " AND LOWER(name) LIKE :sMatch"
            params["sMatch"] = f'%{strMatch.lower()}%'

        if catMatch:
            query += " AND category = :cat"
            params["cat"] = catMatch
        
        if priceSort:
            query += f" ORDER BY price {priceSort}"

        if k:
            query += " LIMIT :limitK"
            params["limitK"] = k

        print(query)

        rows = app.db.execute(query, **params)

        return [Product(*row) for row in rows]

    @staticmethod
    def get_filtered2(available=True, k=0, strMatch="", catMatch = "", priceSort = "", id_spec = ""):

        print(catMatch)

        query = '''
            WITH ProdAvg(pid, avgRating) AS (
                SELECT products.id, ROUND(AVG(rating)::numeric, 2)
                FROM Reviews, Products
                WHERE Reviews.pid = products.id GROUP BY products.id
            )
            SELECT id, name, price, available, description, category, avgRating
            FROM Products, ProdAvg
            WHERE available = :available AND Products.id = ProdAvg.pid
        '''

        params = {"available": available}

        if id_spec:
            query += " AND Products.id = :sMatch"
            params["sMatch"] = id_spec

        if strMatch:
            query += " AND LOWER(name) LIKE :sMatch"
            params["sMatch"] = f'%{strMatch.lower()}%'

        if catMatch:
            query += " AND category = :cat"
            params["cat"] = catMatch
        
        if priceSort:
            query += f" ORDER BY price {priceSort}"

        if k:
            query += " LIMIT :limitK"
            params["limitK"] = k

        print(query)

        rows = app.db.execute(query, **params)

        print(rows)
        return [Product(*row) for row in rows]



    def get_product_info(product_id):


        rows = app.db.execute('''
        SELECT id, name, price, available, description, category
        FROM Products
        WHERE id = :id ORDER BY price
        ''', id = product_id)

        rows = Product.get_filtered2(id_spec = product_id)


        return rows
