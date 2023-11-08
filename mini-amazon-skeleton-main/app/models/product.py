from flask import current_app as app


class Product:
    def __init__(self, id, name, price, available, description, category):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.available = available

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True, k = -1):

        if k > -1:

            rows = app.db.execute('''
    SELECT id, name, price, available, description, category
    FROM Products
    WHERE available = :available ORDER BY price DESC LIMIT :topK
    ''',
                                available=available, topK = k)
        else:
            rows = app.db.execute('''
    SELECT id, name, price, available, description, category
    FROM Products
    WHERE available = :available ORDER BY price DESC
    ''',
                                available=available)

        return [Product(*row) for row in rows]


    def get_product_info(product_id):


        rows = app.db.execute('''
        SELECT id, name, price, available, description, category
        FROM Products
        WHERE id = :id ORDER BY price
        ''', id = product_id)


        return [Product(*row) for row in rows]
