from flask import current_app as app


class InCart:
    def __init__(self, uid, pid, qty):
        self.uid = uid
        self.pid = pid
        self.qty = qty

    @staticmethod
    def get_items_in_cart(uid):
        rows = app.db.execute('''
SELECT uid, pid, qty
FROM InCart
WHERE uid = :uid
''',
                              uid=uid)
        return [InCart(*row) for row in rows]

    @staticmethod
    def addItem(uid, pid, qty):
        rows = app.db.execute("""
INSERT INTO InCart(uid, pid, qty)
VALUES(:uid, :pid, :qty)
""",
                            uid=uid,
                            pid=pid,
                            qty=qty)
        return InCart(*(rows[0])) if rows else None
        # except Exception as e:
        #     # likely email already in use; better error checking and reporting needed;
        #     # the following simply prints the error to the console:
        #     print(str(e))
        #     return None

    @staticmethod
    def deleteItem(uid, pid, qty):
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