from flask import current_app as app

from .product import Product


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
            if Product.get_product_info_from_name(product_name) == None: # product_name doesn't exist --> can't return pid
                return "error" # do nothing; page just refreshes
            wholeThing = Product.get_product_info_from_name(product_name)[0]
            pid, category, description, price, unique_id = wholeThing[0],wholeThing[1],wholeThing[2],wholeThing[3], wholeThing[4]
        # if product_name == "": # user gave pid instead of product_name
        #     if Product.get_product_info_from_pid(pid) == None: # pid doesn't exist --> can't return product_name
        #         return "error"
        #     wholeThing = Product.get_product_info_from_pid(pid)[0]
        #     product_name, category, description, price, unique_id = wholeThing[0],wholeThing[1],wholeThing[2],wholeThing[3], wholeThing[4]
        
        inventory_item = InventoryItem.get_inventory_item_by_pid(unique_id,sid)
        # check that pid doesn't already exist in seller's inventory
        if inventory_item==None: 
            # add another seller's product (from Products) to this seller's Inventory and into Products with this sid
            Product.addOtherSellersProduct(pid, sid, product_name, category, description, price, quantity)
        if inventory_item!=None: 
        #else: # pid does exist in seller's current inventory ==> update quantity of inventory item
            # get quantity of existing product in seller's inventory
            #qty = InventoryItem.get_qty(sid, pid) # should be either 0 or 1 row
            qty = inventory_item[0][3]

            if quantity + qty <= 0:
            # if quantity of product is decreased to 0 or below, then delete product from inventory
                rows = InventoryItem.update_quantity(sid, pid, 0)
            else: 
                # update quantity of existing product (should work for incrementing and decrementing)
                new_quantity = quantity + qty
                rows = InventoryItem.update_quantity(sid, pid, new_quantity)
            return rows if rows else None
        return
    
    @staticmethod
    def get_inventory_item_by_pid(pid,sid):
        try:
            rows = app.db.execute("""
SELECT *
FROM Inventory
WHERE pid = :pid
AND sid=:sid
""",
                                  pid=pid,
                                  sid=sid)
            return rows if rows else None
        except Exception as e:
            print(str(e))
            return None