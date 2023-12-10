from flask import current_app as app

class SellerReview:
    def __init__(self, id, uid, sid, time_posted, rating, review_text, first_name, last_name):
        self.id = id
        self.uid = uid
        self.sid = sid
        # self.sellerId = sellerId
        # self.review_type = review_type
        self.time_posted = time_posted
        self.rating = rating
        self.review_text = review_text
        self.first_name = first_name
        self.last_name = last_name

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
SELECT SellerReviews.id, uid, sid, time_posted, rating, review_text, Users.firstname, Users.lastname
FROM SellerReviews
JOIN Users ON Users.id = SellerReviews.sid
WHERE uid = :uid
ORDER BY time_posted DESC
''', uid = uid)
        return [SellerReview(*row) for row in rows]
    @staticmethod
    def update_review(id, newInput, newInputRating):
        rows = app.db.execute("""
UPDATE SellerReviews
SET review_text = :newInput, time_posted = current_timestamp AT TIME ZONE 'UTC', rating = :newInputRating
WHERE id = :id
""",
                              id=id, newInput=newInput,newInputRating=newInputRating)
    @staticmethod
    def delete_review(id):
        rows = app.db.execute("""
DELETE FROM SellerReviews
WHERE id = :id
""",
                            id=id)
        return rows 
    @staticmethod
    def add_review(uid, sid, time_posted, rating, review_text):
        
        # try:
            rows = app.db.execute("""
INSERT INTO SellerReviews(uid, sid, time_posted, rating, review_text)
VALUES(:uid, :sid, :time_posted, :rating, :review_text)                      
""",
                                  uid=uid,
                                  sid=sid,
                                  time_posted=time_posted, rating=rating, review_text=review_text)
            # id = rows[0][0]
            return rows if rows else None
        # except Exception as e:
        #     # likely email already in use; better error checking and reporting needed;
        #     # the following simply prints the error to the console:
        #     print(str(e))
        #     return None
    def review_exists(uid, sid):
        rows = app.db.execute("""
SELECT *
FROM SellerReviews
WHERE uid = :uid AND sid =:sid
""",
                              uid=uid, sid=sid)
        return len(rows) > 0


    @staticmethod
    def getReviewMetrics(id):

        query = '''
        SELECT COALESCE(COUNT(*), 0), COALESCE(ROUND(AVG(SellerReviews.rating)::numeric, 2), 0.0)
        FROM SellerReviews
        WHERE sid = :id
        '''

        return app.db.execute(query, id = id)[0]
