from flask import current_app as app

class InventoryItem:
    def __init__(self, id, sid, pid, quantity, product_name):
        self.id = id
        self.sid = sid
        self.pid = pid
        self.quantity = quantity
        self.product_name = product_name

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, sid, pid, quantity
FROM Inventory
WHERE id = :id
''',
                              id=id)
        return InventoryItem(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_sid(sid):
        rows = app.db.execute('''
SELECT Inventory.id, sid, pid, quantity, Products.name
FROM Inventory, Products
WHERE sid = :sid 
AND Inventory.pid = Products.id
''',
                              sid=sid)
        return [InventoryItem(*row) for row in rows]