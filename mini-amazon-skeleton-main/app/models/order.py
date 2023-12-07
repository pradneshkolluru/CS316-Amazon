from flask import current_app as app


class Order:
    def __init__(self, id, uid, order_fulfilled):
        self.id = id
        self.uid = uid,
        self.order_fulfilled = order_fulfilled

    @staticmethod
    def get_all_orders_for_user(uid):
        rows = app.db.execute('''
SELECT id, uid, order_fulfilled
FROM Orders
WHERE uid = :uid
''',
                              uid=uid)
        return [Order(*row) for row in rows]
    
    @staticmethod
    def get_all_orders_for_seller(sid):
        rows = app.db.execute('''
SELECT oid, pid, qty, unit_price, purchase_fulfilled, time_purchased
FROM Purchases
WHERE sid = :sid
''',
                              sid=sid)
        return [Order(*row) for row in rows]
    
    @staticmethod
    def get_order_info_for_seller(sid, oid):
        rows = app.db.execute('''
SELECT Purchases.pid, Purchases.qty, Purchases.purchase_fulfilled, Products.name
FROM Purchases, Products
WHERE sid = :sid
AND oid = :oid
AND Purchases.pid = Products.id                              
''',
                              sid=sid,
                              oid=oid)
        return rows if rows else None
    
    @staticmethod
    def get_buyer_info_from_purchase(oid): # for a given oid, find buyer and buyer info
        rows = app.db.execute('''
SELECT DISTINCT Users.firstname, Users.lastname, Users.address, Users.email
FROM Purchases, Users
WHERE Purchases.uid = Users.id
AND Purchases.oid = :oid
''',
                              oid=oid)
        return rows if rows else None