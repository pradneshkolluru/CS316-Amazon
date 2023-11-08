from flask import current_app as app


class InCart:
    def __init__(self, uid, pid, qty):
        self.uid = uid
        self.pid = pid
        self.qty = qty

    @staticmethod
    def get_items_in_cart(uid):
        rows = app.db.execute('''
SELECT pid, name, qty, price
FROM InCart I, Products P
WHERE uid = :uid
    AND I.pid = P.id
''',
                              uid=uid)
        return rows

    @staticmethod
    def get_total_price(uid):
        rows = app.db.execute('''
SELECT SUM(I.qty * P.price)
FROM InCart I, Products P
WHERE uid = :uid
    AND I.pid = P.id
GROUP BY uid
''',
                              uid=uid)
        return rows[0][0] if rows else None

    @staticmethod
    def add_item_to_cart(uid, pid, qty):
        qty_in_cart = app.db.execute("""
SELECT *
FROM InCart
WHERE uid = :uid AND pid = :pid
""",
                            uid=uid,
                            pid=pid)

        if len(qty_in_cart) == 0:
            rows = app.db.execute("""
INSERT INTO InCart(uid, pid, qty)
VALUES(:uid, :pid, :qty)
""",
                            uid=uid,
                            pid=pid,
                            qty=qty)
        else:
            rows = app.db.execute("""
UPDATE InCart
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
SELECT qty FROM InCart
WHERE uid = :uid
        AND pid = :pid
        AND qty = :qty)
 """,
                            uid=uid,
                            pid=pid,
                            qty=qty)
        if qty > old_qty:
            rows = app.db.execute("""
DELETE FROM InCart
WHERE uid = :uid
        AND pid = :pid
        AND qty = :qty)
""",
                            uid=uid,
                            pid=pid,
                            qty=qty)
        else:
            rows = app.db.execute("""
UPDATE InCart
SET qty = :new_qty
WHERE uid = :uid
        AND pid = :pid
""",
                            new_qty=old_qty-qty,
                            uid = uid,
                            pid = pid)
        return InCart(*(rows[0])) if rows else None