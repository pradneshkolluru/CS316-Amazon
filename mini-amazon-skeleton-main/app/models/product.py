from flask import current_app as app
import io
import base64
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from sqlalchemy import text
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
    def __init__(self, id, name, price, available, description, category, avgRating = 0, 
                 image = "/static/images/gargi.jpeg", quantity = None, sid = None, firstname = '', lastname = ''):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.available = available
        self.avgRating = avgRating
        self.image = image
        self.quantity = quantity
        self.sid = sid
        self.firstname = firstname
        self.lastname = lastname

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

        rows = app.db.execute(query, **params)

        return [Product(*row) for row in rows]

    @staticmethod
    def get_filtered2(available=True, k=0, strMatch="", catMatch = "", priceSort = "", id_spec = ""):

        query = '''
            WITH ProdAvg AS (
                SELECT Products.id AS pid, 
                COALESCE(ROUND(AVG(Reviews.rating)::numeric, 2), 0.0) AS avgRating
                FROM Products
                LEFT JOIN Reviews ON Reviews.pid = Products.id
                GROUP BY Products.id)
            SELECT Products.id, name, price, available, description, category, avgRating, image_path, '' quantity, sid, firstname, lastname
            FROM Products, ProdAvg, Users
            WHERE available = :available AND Products.id = ProdAvg.pid AND Products.sid = Users.id
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

        rows = app.db.execute(query, **params)

        return [Product(*row) for row in rows]



    def get_product_info(id_specif):


        rows = Product.get_filtered2(id_spec = id_specif)

        return rows
    

    def getProductsFromOtherVenders(uId):

        query = '''
        WITH ProdAvg AS (
        SELECT 
        Seller.uid AS sellerID, 
        COALESCE(ROUND(AVG(SellerReviews.rating)::numeric, 2), 0.0) AS avgRating
        FROM Seller
        LEFT JOIN SellerReviews ON SellerReviews.sid = Seller.uid
        GROUP BY Seller.uid
        ),
        getPid AS (
        SELECT Products.product_id AS boppid
        FROM Products
        WHERE Products.id = :id
        )
        SELECT Products.id, Products.name, Products.price, Products.available, Products.description, Products.category, avgRating, Products.image_path, Inventory.quantity, Products.sid, Users.firstname, Users.lastname
        FROM getPid
        INNER JOIN Products ON Products.product_id = getPid.boppid
        INNER JOIN Inventory ON Products.id = Inventory.pid
        INNER JOIN ProdAvg ON ProdAvg.sellerID = Inventory.sid
        INNER JOIN Users ON Users.id = Inventory.sid
        WHERE Products.available = TRUE
        ORDER BY Products.price;
        '''


        rows = app.db.execute(query, id = uId)

        return [Product(*row) for row in rows]

    @staticmethod
    def addNewProduct(sid, name, category, description, price, quantity):

        getMaxPidQuery = '''
        SELECT MAX(product_id)
        FROM Products
        '''

        pid = app.db.execute(getMaxPidQuery)[0][0] + 1
        

        addPatientQuery = '''
        INSERT INTO Products(product_id, sid, name, category, description, price, image_path)
        VALUES(:pid, :sid, :name, :cat, :des, :price, :image_path)
        RETURNING id    
        '''

        divyas_id = app.db.execute(addPatientQuery, pid = pid,
                                                    sid = sid,
                                                    name = name,
                                                    cat = category, 
                                                    des = description,
                                                    price = price,
                                                    image_path = f'/static/images/{category}/1.jpeg')[0][0]


        insertIntoInventory = '''
        INSERT INTO Inventory(sid, pid, quantity)
        VALUES(:sid, :pid, :quantity)
        RETURNING sid, pid    
        '''

        rows = app.db.execute(insertIntoInventory, sid = sid,
                                                   pid = divyas_id,
                                                   quantity = quantity)
    @staticmethod
    def addOtherSellersProduct(pid, sid, name, category, description, price, quantity):

        addPatientQuery = '''
        INSERT INTO Products(product_id, sid, name, category, description, price, image_path)
        VALUES(:pid, :sid, :name, :cat, :des, :price, :image_path)
        RETURNING id    
        '''

        divyas_id = app.db.execute(addPatientQuery, pid = pid,
                                                    sid = sid,
                                                    name = name,
                                                    cat = category, 
                                                    des = description,
                                                    price = price,
                                                    image_path = f'/static/images/{category}/1.jpeg')[0][0]


        insertIntoInventory = '''
        INSERT INTO Inventory(sid, pid, quantity)
        VALUES(:sid, :pid, :quantity)
        RETURNING sid, pid    
        '''

        rows = app.db.execute(insertIntoInventory, sid = sid,
                                                   pid = divyas_id,
                                                   quantity = quantity)

    @staticmethod
    def get_product_info_from_name(product_name):
        try:
            rows = app.db.execute("""
SELECT product_id, category, description, price,id
FROM Products
WHERE LOWER(name) = :p_name
LIMIT 1
""",
                                  p_name = product_name)
            return rows if rows else None
        except Exception as e:
            print(str(e))
            return None
        
    @staticmethod
    def get_product_info_from_pid(pid):
        try:
            rows = app.db.execute("""
SELECT name, category, description, price, id
FROM Products
WHERE product_id = :pid
LIMIT 1
""",
                                  pid = pid)
            return rows if rows else None
        except Exception as e:
            print(str(e))
            return None
    @staticmethod
    def recommendations(category):
        rows = app.db.execute("""
select 
from products
where category = :category
limit 3
""",
                            category=category)
        return [Product(*row) for row in rows]

    
    @staticmethod
    def updateProduct(uid, changeField, newInput):

        query = text(f'''
        UPDATE Products
        SET {changeField} = :newInput
        WHERE id = :id
        ''')

        rows = app.db.execute(str(query.compile()), id=uid, newInput=newInput)

    @staticmethod
    def get_by_sid(sid):

        query = '''
            WITH ProdAvg AS (
                SELECT Products.id AS pid, 
                COALESCE(ROUND(AVG(Reviews.rating)::numeric, 2), 0.0) AS avgRating
                FROM Products
                LEFT JOIN Reviews ON Reviews.pid = Products.id
                GROUP BY Products.id)
            SELECT id, name, price, available, description, category, avgRating, image_path
            FROM Products, ProdAvg
            WHERE sid = :sid AND Products.id = ProdAvg.pid
        '''
        rows = app.db.execute(query, sid=sid)
        return [Product(*row) for row in rows] if rows is not None else None
