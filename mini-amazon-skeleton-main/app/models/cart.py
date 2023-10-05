from flask import current_app as app


class Cart:
    def __init__(self, uid, curr_total_price):
        self.uid = uid
        self.curr_total_price = curr_total_price

    @staticmethod
    def get_total(uid):
        rows = app.db.execute('''
SELECT uid, curr_total_price
FROM Cart
WHERE uid = :uid
''',
                              uid=uid)
        return Cart(*(rows[0])).curr_total_price if rows else None