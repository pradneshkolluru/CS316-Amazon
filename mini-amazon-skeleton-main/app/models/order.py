from flask import current_app as app


class Order:
    def __init__(self, id, uid, order_fulfilled):
        self.id = id
        self.uid = uid
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
    def get_all_purchases_in_orders(uid):
        rows = app.db.execute('''
SELECT O.id, O.uid, P.pid, P.qty, Pr.name, P.unit_price, P.purchase_fulfilled, O.order_fulfilled
FROM Orders O, Purchases P, Products Pr
WHERE O.id = P.oid 
    AND P.pid = Pr.id
    AND O.uid = :uid
''',
                            uid =uid)
        return rows if rows else None