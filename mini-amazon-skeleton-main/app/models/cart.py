from flask import current_app as app

from .inventory import InventoryItem
from .order import Order
from .purchase import Purchase

class Cart:
    def __init__(self, uid, pid, sid, product_name, qty, unit_price):
        self.uid = uid
        self.pid = pid
        self.sid = sid
        self.qty = qty
        self.product_name = product_name
        self.unit_price = unit_price

    @staticmethod
    def get_items_in_cart(uid):
        rows = app.db.execute('''
SELECT uid, pid, sid, name, qty, price
FROM Cart C, Products P
WHERE uid = :uid
    AND C.pid = P.id
''',
                              uid=uid)
        return [Cart(*row) for row in rows]

    @staticmethod
    def get_total_price(uid):
        rows = app.db.execute('''
SELECT SUM(C.qty * P.price)
FROM Cart C, Products P
WHERE uid = :uid
    AND C.pid = P.id
GROUP BY uid
''',
                              uid=uid)
        return rows[0][0] if rows else None

    @staticmethod
    def update_item_qty(uid, pid, qty):
        qty_in_cart = Cart.get_qty_in_cart(uid, pid)

        if len(qty_in_cart) == 0:
        # if qty_in_cart == None:
            rows = app.db.execute("""
INSERT INTO Cart(uid, pid, qty)
VALUES(:uid, :pid, :qty)
""",
                            uid=uid,
                            pid=pid,
                            qty=qty)
        elif qty_in_cart[0][0] + qty <= 0:
            rows = Cart.delete_item_from_cart(uid, pid)
        else:
            rows = app.db.execute("""
UPDATE Cart
SET qty = qty + :add_qty
WHERE uid = :uid 
    AND pid = :pid
""",
                            add_qty=qty,
                            uid=uid,
                            pid=pid)
        return rows if rows else None

    @staticmethod
    def delete_item_from_cart(uid, pid):
        rows = app.db.execute("""
DELETE FROM Cart
WHERE uid = :uid
        AND pid = :pid
""",
                            uid=uid,
                            pid=pid)
        return rows
    
    @staticmethod
    def get_qty_in_cart(uid, pid):
        qty = app.db.execute("""
SELECT qty
FROM Cart
WHERE uid = :uid AND pid = :pid
""",
                            uid=uid,
                            pid=pid)
        return qty
    
    @staticmethod
    def submit_cart(uid):
        items_in_cart = Cart.get_items_in_cart(uid)
        enough_inventory = True
        
        for item in items_in_cart:
            qty_in_inventory = InventoryItem.get_qty(item.sid, item.pid)
            if qty_in_inventory < item.qty:
                enough_inventory = False
        
        if enough_inventory:
            new_order = Order.add_new_order(uid)
            oid = new_order[0][0]
            for item in items_in_cart:
                InventoryItem.update_quantity(item.sid, item.pid, item.qty*-1)
                Purchase.add_new_purchase(uid, item.pid, oid, item.qty, item.sid, item.unit_price)
                # delete from cart
            return "Cart Submitted!"
        else:
            return "There is not enough inventory for one or more of your items. Please check and try again."

