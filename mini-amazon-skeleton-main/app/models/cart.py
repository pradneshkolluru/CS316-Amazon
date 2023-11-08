from flask import current_app as app


class Cart:
    def __init__(self, uid, pid, qty):
        self.uid = uid
        self.pid = pid
        self.qty = qty

#     @staticmethod
#     def get_total(uid):
#         rows = app.db.execute('''
# SELECT uid, curr_total_price
# FROM Cart
# WHERE uid = :uid
# ''',
#                               uid=uid)
#         return Cart(*(rows[0])).curr_total_price if rows else None
    @staticmethod
    def get_items_in_cart(uid):
        rows = app.db.execute('''
SELECT pid, name, qty, price
FROM Cart C, Products P
WHERE uid = :uid
    AND C.pid = P.id
''',
                              uid=uid)
        return rows

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
    def add_item_to_cart(uid, pid, qty):
        qty_in_cart = app.db.execute("""
SELECT *
FROM Cart
WHERE uid = :uid AND pid = :pid
""",
                            uid=uid,
                            pid=pid)

        if len(qty_in_cart) == 0:
            rows = app.db.execute("""
INSERT INTO Cart(uid, pid, qty)
VALUES(:uid, :pid, :qty)
""",
                            uid=uid,
                            pid=pid,
                            qty=qty)
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
    def delete_item_from_cart(uid, pid, qty):
        old_qty = app.db.execute("""
SELECT qty FROM Cart
WHERE uid = :uid
        AND pid = :pid
        AND qty = :qty)
 """,
                            uid=uid,
                            pid=pid,
                            qty=qty)
        if qty > old_qty:
            rows = app.db.execute("""
DELETE FROM Cart
WHERE uid = :uid
        AND pid = :pid
        AND qty = :qty)
""",
                            uid=uid,
                            pid=pid,
                            qty=qty)
        else:
            rows = app.db.execute("""
UPDATE Cart
SET qty = :new_qty
WHERE uid = :uid
        AND pid = :pid
""",
                            new_qty=old_qty-qty,
                            uid = uid,
                            pid = pid)
        return Cart(*(rows[0])) if rows else None