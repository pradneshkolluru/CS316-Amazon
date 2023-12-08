from flask import current_app as app


class Purchase:
    def __init__(self, id, uid, pid, time_purchased):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_purchased = time_purchased

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT P.id, P.uid, P.pid, O.time_purchased
FROM Purchases P, Orders O
WHERE P.id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT P.id, P.uid, P.pid, O.time_purchased
FROM Purchases P, Orders O
WHERE P.uid = :uid
AND O.time_purchased >= :since
ORDER BY O.time_purchased DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]
    @staticmethod 
    def get_all(uid):
        rows = app.db.execute('''
SELECT P.id, P.uid, P.pid, O.time_purchased
FROM Purchases P, Orders O
WHERE P.uid = :uid
ORDER BY O.time_purchased DESC
''',
                              uid=uid)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def add_new_purchase(uid, pid, oid, qty, sid, unit_price):
        rows = app.db.execute('''
INSERT INTO Purchases(uid, pid, oid, qty, purchase_fulfilled, sid, unit_price)
VALUES(:uid, :pid, :oid, :qty, :purchase_fulfilled, :sid, :unit_price)
''',
                                uid=uid,
                                pid=pid,
                                oid=oid,
                                qty=qty,
                                purchase_fulfilled=False,
                                sid=sid,
                                unit_price=unit_price)
        return rows if rows else None
        