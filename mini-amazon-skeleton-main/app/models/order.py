from flask import current_app as app


class Order:
    def __init__(self, oid, uid, pid, sid, qty, product_name, unit_price, time_purchased, purchase_fulfilled, order_fulfilled, sellerfirst, sellerlast):
        self.oid = oid
        self.uid = uid
        self.pid = pid
        self.sid = sid
        self.qty = qty
        self.product_name = product_name
        self.unit_price = unit_price
        self.time_purchased = time_purchased
        self.purchase_fulfilled = purchase_fulfilled
        self.order_fulfilled = order_fulfilled
        self.sellerfirst = sellerfirst
        self.sellerlast = sellerlast

    @staticmethod
    def get_items_in_order(uid, oid):
        rows = app.db.execute('''
SELECT O.id, O.uid, P.pid, P.sid, P.qty, Pr.name, P.unit_price, P.time_purchased, P.purchase_fulfilled, O.order_fulfilled, U.firstname, U.lastname
FROM Orders O, Purchases P, Products Pr, Users U
WHERE O.id = P.oid 
    AND P.pid = Pr.id
    AND O.uid = :uid
    AND O.id = :oid
    AND U.id = P.sid
''',
                              uid=uid,
                              oid=oid)
        # return rows if rows else None
        return [Order(*row) for row in rows]
    
    @staticmethod
    def get_all_purchases_in_orders(uid):
        rows = app.db.execute('''
SELECT O.id, O.uid, P.pid, P.sid, P.qty, Pr.name, P.unit_price, P.time_purchased, P.purchase_fulfilled, O.order_fulfilled,  U.firstname, U.lastname
FROM Orders O, Purchases P, Products Pr, Users U
WHERE O.id = P.oid 
    AND P.pid = Pr.id
    AND O.uid = :uid
    AND U.id = P.sid
''',
                            uid =uid)
        # return rows if rows else None
        return [Order(*row) for row in rows]
    
    @staticmethod
    def add_new_order(uid):
        rows = app.db.execute("""
INSERT INTO Orders(uid, order_fulfilled)
VALUES(:uid, :order_fulfilled)
""",
                            uid=uid,
                            order_fulfilled=False)
        return rows if rows else None
    @staticmethod
    def get_filtered( k=0, strMatch="", uid=-1, sellerMatch=""):
        query = '''
SELECT O.id, O.uid, P.pid, P.sid, P.qty, Pr.name, P.unit_price, P.time_purchased, P.purchase_fulfilled, O.order_fulfilled, U.firstname, U.lastname
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

        if k:
            query += " ORDER BY unit_price ASC LIMIT :limitK"
            params["limitK"] = k

        if sellerMatch:
            query += " AND LOWER(lastname) LIKE :sellerMatch"
            params["sellerMatch"] = f'%{sellerMatch.lower()}%'

        rows = app.db.execute(query, **params)
        return [Order(*row) for row in rows]