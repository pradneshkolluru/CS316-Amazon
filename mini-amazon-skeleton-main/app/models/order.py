from flask import current_app as app


class Order:
    def __init__(self, oid, uid, pid, sid, qty, product_name, unit_price, total_order_price, time_purchased, purchase_fulfilled, time_fulfilled, order_fulfilled, sellerfirst, sellerlast):
        self.oid = oid
        self.uid = uid
        self.pid = pid
        self.sid = sid
        self.qty = qty
        self.product_name = product_name
        self.unit_price = unit_price
        self.total_order_price = total_order_price
        self.time_purchased = time_purchased
        self.purchase_fulfilled = purchase_fulfilled
        self.time_fulfilled = time_fulfilled
        self.order_fulfilled = order_fulfilled
        self.sellerfirst = sellerfirst
        self.sellerlast = sellerlast

    @staticmethod
    def get_order_info(uid, oid):
        rows = app.db.execute('''
SELECT id, uid, order_fulfilled, time_purchased, total_price
FROM Orders
WHERE uid = :uid
    AND id = :oid
''',
                              uid=uid,
                              oid=oid)
        return rows if rows else None


    @staticmethod
    def get_items_in_order(oid):
        rows = app.db.execute('''
SELECT O.id, O.uid, P.pid, P.sid, P.qty, Pr.name, P.unit_price, O.total_price, O.time_purchased, P.purchase_fulfilled, P.time_fulfilled, O.order_fulfilled, U.firstname, U.lastname
FROM Orders O, Purchases P, Products Pr, Users U
WHERE O.id = P.oid 
    AND P.pid = Pr.id
    AND O.id = :oid
    AND U.id = P.sid
''',
                              oid=oid)
        return [Order(*row) for row in rows]
    
    @staticmethod
    def get_all_orders_for_seller(sid):
        rows = app.db.execute('''
SELECT P.oid, P.pid, P.qty, P.unit_price, P.purchase_fulfilled, O.time_purchased
FROM Purchases P, Orders O
WHERE P.sid = :sid
AND P.oid = O.id
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
SELECT O.id, O.uid, P.pid, P.sid, P.qty, Pr.name, P.unit_price, O.total_price, O.time_purchased, P.purchase_fulfilled, P.time_fulfilled, O.order_fulfilled, U.firstname, U.lastname
FROM Orders O, Purchases P, Products Pr, Users U
WHERE O.id = P.oid 
    AND P.pid = Pr.id
    AND O.uid = :uid
    AND U.id = P.sid
''',
                            uid =uid)
        return [Order(*row) for row in rows]
    
    @staticmethod
    def add_new_order(uid, total_cart_price):
        rows = app.db.execute("""
INSERT INTO Orders(uid, order_fulfilled, total_price)
VALUES(:uid, :order_fulfilled, :total_price)
RETURNING id
""",
                            uid=uid,
                            order_fulfilled=False,
                            total_price=total_cart_price)
        return rows if rows else None

    @staticmethod
    def check_and_update_order_fulfillment(oid):
        purchases = Order.get_items_in_order(oid)
        for purchase in purchases:
            if not purchase.purchase_fulfilled:
                return None
        
        rows = app.db.execute("""
UPDATE Orders
SET order_fulfilled = True
WHERE id = :oid
""",
                            oid=oid)
        return rows if rows else None

    @staticmethod
    def update_purchase_fulfillment(oid, pid, new_status):
        rows = app.db.execute("""
UPDATE Purchases
SET purchase_fulfilled = :new_status
WHERE oid = :oid
AND pid = :pid
""",
                            oid=oid,
                            pid=pid,
                            new_status=new_status)
        return rows if rows else None
    
    @staticmethod
    def update_purchase_fulfillment_time(oid, pid, click_time):
        rows = app.db.execute("""
UPDATE Purchases
SET time_fulfilled = :click_time
WHERE oid = :oid
AND pid = :pid
""",
                            oid=oid,
                            pid=pid,
                            click_time=click_time)
        return rows if rows else None
    
    @staticmethod
    def get_filtered(strMatch="", uid=-1, sellerMatch="", year=""):
        query = '''
SELECT O.id, O.uid, P.pid, P.sid, P.qty, Pr.name, P.unit_price, O.total_price, O.time_purchased, P.purchase_fulfilled, P.time_fulfilled, O.order_fulfilled, U.firstname, U.lastname
FROM Orders O, Purchases P, Products Pr, Users U
WHERE O.id = P.oid 
    AND P.pid = Pr.id
    AND O.uid = :uid
    AND U.id = P.sid
        '''

        params = {"uid":uid}

        if strMatch:
            query += " AND LOWER(name) LIKE :sMatch"
            params["sMatch"] = f'%{strMatch.lower()}%'

        if sellerMatch:
            query += " AND LOWER(lastname) LIKE :sellerMatch"
            params["sellerMatch"] = f'%{sellerMatch.lower()}%'
        if year:
             query += " AND Extract('Year' FROM Time_purchased) = :year"
             params["year"] = year

        rows = app.db.execute(query, **params)
        return [Order(*row) for row in rows]
    
    @staticmethod
    def get_years(uid):
        rows = app.db.execute("""
SELECT DISTINCT EXTRACT ('Year' FROM Time_purchased)
FROM Orders
WHERE uid = :uid
""",
                            uid=uid)
        return [int(*row) for row in rows] if rows else None
    
    @staticmethod
    def filter_oid(sid, strMatch=""):
        query = """
SELECT P.oid, P.pid, P.qty, P.unit_price, P.purchase_fulfilled, O.time_purchased
FROM Purchases P, Orders O
WHERE P.sid = :sid
"""     
        if strMatch:
            query += " AND P.oid = :strMatch"
        rows = app.db.execute(query,sid=sid,strMatch=strMatch )
        return rows if rows else None