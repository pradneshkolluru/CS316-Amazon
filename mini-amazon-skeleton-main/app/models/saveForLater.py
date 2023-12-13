from flask import current_app as app
from flask import flash

from .inventory import InventoryItem
from .order import Order
from .purchase import Purchase
from .user import User

class SaveForLater:
    def __init__(self, uid, pid, product_name, unit_price, image_path):
        self.uid = uid
        self.pid = pid
        self.product_name = product_name
        self.unit_price = unit_price
        self.image_path = image_path

    @staticmethod
    def get_saved_items(uid):
        rows = app.db.execute('''
SELECT uid, pid, name, price, image_path
FROM SaveForLater S, Products P
WHERE uid = :uid
    AND S.pid = P.id
''',
                              uid=uid)
        return [SaveForLater(*row) for row in rows]
    
    @staticmethod
    def add_item_to_saved(uid, pid):
        rows = app.db.execute("""
INSERT INTO SaveForLater(uid, pid)
VALUES(:uid, :pid)
""",
                                  uid=uid,
                                  pid=pid)
        return rows if rows else None
    
    @staticmethod
    def delete_from_saved(uid, pid):
        rows = app.db.execute("""
DELETE FROM SaveForLater
WHERE uid = :uid
    AND pid = :pid
""",
                            uid=uid,
                            pid=pid)
        return rows