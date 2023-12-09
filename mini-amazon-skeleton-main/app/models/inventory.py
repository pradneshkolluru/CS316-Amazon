from flask import current_app as app

class InventoryItem:
    #def __init__(self, id, sid, pid, quantity, product_name, product_price):
    def __init__(self, id, sid, pid, quantity, product_name, product_price, description, **kwargs):
        self.id = id
        self.sid = sid
        self.pid = pid
        self.quantity = quantity
        self.product_name = product_name
        self.product_price = product_price
        self.description = description

#     @staticmethod
#     def get(id):
#         rows = app.db.execute('''
# SELECT id, sid, pid, quantity
# FROM Inventory
# WHERE id = :id
# ''',
#                               id=id)
#         return InventoryItem(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_sid(sid):
        rows = app.db.execute('''
SELECT Inventory.id, Inventory.sid, pid, quantity, Products.name, Products.price, Products.description
FROM Inventory, Products
WHERE Inventory.sid = :sid 
AND Inventory.pid = Products.id
''',
                              sid=sid)
        return [InventoryItem(*row) for row in rows]
    
    @staticmethod
    def get_all_products_by_sid(sid):
        rows = app.db.execute('''
SELECT pid
FROM Inventory, Products
WHERE Inventory.sid = :sid 
AND Inventory.pid = Products.id
''',
                              sid=sid)
        return rows if rows else None

    @staticmethod
    def add_new_item(sid, pid, quantity):
        # adding new product id to inventory with an initial quantity
        try:
            rows = app.db.execute("""
INSERT INTO Inventory(sid, pid, quantity)
VALUES(:sid, :pid, :quantity)
""",
                                  sid=sid,
                                  pid=pid,
                                  quantity = quantity)
            return rows if rows else None
        except Exception as e:
            print(str(e))
            return None
        
    @staticmethod
    def get_pid(product_name):
        try:
            rows = app.db.execute("""
SELECT id
FROM Products
WHERE name = :p_name
""",
                                  p_name = product_name.capitalize())
            return rows if rows else None
        except Exception as e:
            print(str(e))
            return None
        
    @staticmethod
    def get_qty(sid, pid):
        try:
            rows = app.db.execute("""
SELECT quantity
FROM Inventory
WHERE sid = :sid
AND pid = :pid
""",
                                  sid=sid,
                                  pid=pid)
            return rows if rows else None
        except Exception as e:
            print(str(e))
            return None
             
    @staticmethod
    def update_quantity(sid, pid, quantity):
        # updating quantity of existing product in inventory (quantity parameter is the updated/new quantity)
        try:
            rows = app.db.execute("""
UPDATE Inventory
SET quantity = :quantity
WHERE sid = :sid
AND pid = :pid
""",
                                  sid=sid,
                                  pid=pid,
                                  quantity = quantity)
            return rows if rows else None
        except Exception as e:
            print(str(e))
            return None
        
    @staticmethod
    def delete_item(sid, pid):
        try:
            rows = app.db.execute("""
DELETE FROM Inventory
WHERE sid = :sid
AND pid = :pid
""",
                                  sid=sid,
                                  pid=pid)
            return rows if rows else None
        except Exception as e:
            print(str(e))
            return None
        
        
    @staticmethod
    def update_inventory(sid, quantity, pid=None, product_name=""): # quantity parameter is the number being added / deleted to existing quantity in inventory

        if pid == None: # user gave product_name instead of pid
            if InventoryItem.get_pid(product_name) == None: # pid doesn't exist --> product name doesn't exist
                return "error" # do nothing; page just refreshes
            pid = InventoryItem.get_pid(product_name)[0][0]
            
        # get quantity of existing product in seller's inventory
        qty = InventoryItem.get_qty(sid, pid) # should be either 0 or 1 row
        if qty == None: 
            # pid not currently in sid's inventory (add new product to inventory)
            # product_name is given by user to add new product
            # input product_name has to be already existing (Products relation)
            rows = InventoryItem.add_new_item(sid, pid, quantity)
        elif (quantity + qty[0][0] <= 0):
            # if quantity of product is decreased to 0 or below, then delete product from inventory
            rows = InventoryItem.delete_item(sid, pid)
        else: 
            # update quantity of existing product (should work for incrementing and decrementing)

            new_quantity = quantity + qty[0][0]
            rows = InventoryItem.update_quantity(sid, pid, new_quantity)
        return rows if rows else None