from flask import current_app as app

class SellerReview:
    def __init__(self, id, uid, sid, time_posted, rating, review_text):
        self.id = id
        self.uid = uid
        self.sid = sid
        # self.sellerId = sellerId
        # self.review_type = review_type
        self.time_posted = time_posted
        self.rating = rating
        self.review_text = review_text

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, sid, time_posted
FROM SellerReviews
JOIN Users ON Users.id = SellerReviews.uid
WHERE id = :id
''',
                              id=id)
        return SellerReview(*(rows[0])) if rows else None

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
SELECT SellerReviews.id, uid, sid, time_posted, rating, review_text
FROM SellerReviews
JOIN Users ON Users.id = SellerReviews.sid
WHERE uid = :uid
ORDER BY time_posted DESC
''', uid = uid)
        return [SellerReview(*row) for row in rows]