from flask import current_app as app


class Order:
    def __init__(self, oid, uid, pid, sid, qty, product_name, unit_price, time_purchased, purchase_fulfilled, time_fulfilled, order_fulfilled):
        self.oid = oid
        self.uid = uid
        self.pid = pid
        self.sid = sid
        self.qty = qty
        self.product_name = product_name
        self.unit_price = unit_price
        self.time_purchased = time_purchased
        self.purchase_fulfilled = purchase_fulfilled
        self.time_fulfilled = time_fulfilled
        self.order_fulfilled = order_fulfilled
    
    @staticmethod
    def get_order_info(uid, oid):
        rows = app.db.execute('''
SELECT id, uid, order_fulfilled, time_purchased
FROM Orders
WHERE uid = :uid
    AND id = :oid
''',
                              uid=uid,
                              oid=oid)
        return rows if rows else None


    @staticmethod
    def get_items_in_order(uid, oid):
        rows = app.db.execute('''
SELECT O.id, O.uid, P.pid, P.sid, P.qty, Pr.name, P.unit_price, O.time_purchased, P.purchase_fulfilled, P.time_fulfilled, O.order_fulfilled
FROM Orders O, Purchases P, Products Pr
WHERE O.id = P.oid 
    AND P.pid = Pr.id
    AND O.uid = :uid
    AND O.id = :oid
''',
                              uid=uid,
                              oid=oid)
        return [Order(*row) for row in rows]
    
    @staticmethod
    def get_all_orders_for_seller(sid):
        rows = app.db.execute('''
SELECT oid, pid, qty, unit_price, purchase_fulfilled, time_purchased
FROM Purchases
WHERE sid = :sid
''',
                              sid=sid)
        return rows if rows else None
    
    @staticmethod
    def get_order_info_for_seller(sid, oid):
        rows = app.db.execute('''
SELECT Purchases.pid, Purchases.qty, Purchases.purchase_fulfilled, Products.name
FROM Purchases, Products
WHERE Purchases.sid = :sid
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
    
    @staticmethod
    def get_all_purchases_in_orders(uid):
        rows = app.db.execute('''
SELECT O.id, O.uid, P.pid, P.sid, P.qty, Pr.name, P.unit_price, O.time_purchased, P.purchase_fulfilled, P.time_fulfilled, O.order_fulfilled
FROM Orders O, Purchases P, Products Pr
WHERE O.id = P.oid 
    AND P.pid = Pr.id
    AND O.uid = :uid
''',
                            uid =uid)
        return [Order(*row) for row in rows]
    
    @staticmethod
    def add_new_order(uid):
        rows = app.db.execute("""
INSERT INTO Orders(uid, order_fulfilled)
VALUES(:uid, :order_fulfilled)
RETURNING id
""",
                            uid=uid,
                            order_fulfilled=False)
        return rows if rows else None

    @staticmethod
    def check_and_update_order_fulfillment(uid, oid):
        purchases = Order.get_items_in_order(uid, oid)
        for purchase in purchases:
            if not purchase.purchase_fulfilled:
                return
        
        rows = app.db.execute("""
UPDATE Orders
SET order_fulfilled = True
WHERE uid = :uid 
    AND oid = :oid
""",
                            uid=uid,
                            oid=oid)
        
        return
