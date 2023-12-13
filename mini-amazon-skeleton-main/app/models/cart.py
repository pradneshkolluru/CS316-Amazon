from flask import current_app as app
from flask import flash

from .inventory import InventoryItem
from .order import Order
from .purchase import Purchase
from .user import User

class Cart:
    def __init__(self, uid, pid, sid, product_name, qty, unit_price, image_path):
        self.uid = uid
        self.pid = pid
        self.sid = sid
        self.qty = qty
        self.product_name = product_name
        self.unit_price = unit_price
        self.image_path = image_path

    @staticmethod
    def get_items_in_cart(uid):
        rows = app.db.execute('''
SELECT uid, pid, sid, name, qty, price, image_path
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
    def delete_all_user_items_from_cart(uid):
        rows = app.db.execute("""
DELETE FROM Cart
WHERE uid = :uid
""",
                            uid=uid)
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
        buyer = User.get(uid)

        enough_inventory = True
        total_cart_price = Cart.get_total_price(uid)
        
        # check if all sellers have enough inventory - if even one seller doesn't have enough, don't submit cart
        for item in items_in_cart:
            qty_in_inventory = InventoryItem.get_qty(item.sid, item.pid)
            if qty_in_inventory == None or qty_in_inventory[0][0] < item.qty:
                enough_inventory = False
                flash("There is not enough inventory for product: {p_name}. Please check and try again.".format(p_name = item.product_name))
                return False
        
        if buyer.balance < total_cart_price:
            flash("There isn't enough money in your account to make this order.")
            return False

        if enough_inventory:
            # add to Orders table and get corresponding order id
            new_order = Order.add_new_order(uid, total_cart_price)
            oid = new_order[0][0]

            # decrement buyer balance
            User.update_balance(uid, buyer.balance - total_cart_price)

            for item in items_in_cart:
                # update seller inventory for product
                qty_in_inventory = InventoryItem.get_qty(item.sid, item.pid)
                new_quantity = qty_in_inventory[0][0] - item.qty
                InventoryItem.update_quantity(item.sid, item.pid, new_quantity)

                # add product to Purchases table
                Purchase.add_new_purchase(uid, item.pid, oid, item.qty, item.sid, item.unit_price)

                # increment seller balance
                items_total_price = item.qty * item.unit_price
                seller = User.get(item.sid)
                User.update_balance(item.sid, seller.balance + items_total_price)
            
            # clear cart for user
            Cart.delete_all_user_items_from_cart(uid)

            return oid
        else:
            return False

