from flask import current_app as app


class Product:
    def __init__(self, id, name, price, available, description, category, avgRating):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.available = available
        self.avgRating = avgRating

    @staticmethod
    def get(id):

        query = '''
            SELECT id, name, price, available
            FROM Products
            WHERE id = :id
        '''
        rows = app.db.execute(query, id=id)
        return Product(*(rows[0])) if rows is not None else None
    

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

    
    def get_filtered2(available=True, k=0, strMatch="", catMatch = "", priceSort = ""):

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



    def get_product_info(product_id):


        rows = app.db.execute('''
        SELECT id, name, price, available, description, category
        FROM Products
        WHERE id = :id ORDER BY price
        ''', id = product_id)


        return [Product(*row) for row in rows]
