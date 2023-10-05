from flask import current_app as app

class Review:
    def __init__(self, id, uid, pid, review_type, time_posted, rating, review_text):
        self.id = id
        self.uid = uid
        self.pid = pid
        # self.sellerId = sellerId
        self.review_type = review_type
        self.time_posted = time_posted
        self.rating = rating
        self.review_text = review_text

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_posted
FROM Reviews
WHERE id = :id
''',
                              id=id)
        return Review(*(rows[0])) if rows else None

#     @staticmethod
#     def get_all_by_uid_since(uid, since):
#         rows = app.db.execute('''
# SELECT id, uid, pid, time_posted
# FROM Reviews
# WHERE uid = :uid
# AND time_posted >= :since
# ORDER BY time_posted DESC
# ''',
#                               uid=uid,
#                               since=since)
#         return [Review(*row) for row in rows]

    @staticmethod 
    def get_all(uid):
        rows = app.db.execute('''
SELECT *
FROM Reviews
WHERE uid = :uid
ORDER BY time_posted DESC
''',
                              uid=uid)
        return [Review(*row) for row in rows]
