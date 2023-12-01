from flask import current_app as app

class Review:
    def __init__(self, id, uid, pid, time_posted, rating, review_text, name, firstname):
        self.id = id
        self.uid = uid
        self.pid = pid
        # self.sellerId = sellerId
        # self.review_type = review_type
        self.time_posted = time_posted
        self.rating = rating
        self.review_text = review_text
        self.name = name
        self.firstname = firstname

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_posted
FROM Reviews
JOIN Products ON Products.pit = Reviews.pid
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
SELECT Reviews.id, uid, pid, time_posted, rating, review_text, Products.name
FROM Reviews
JOIN Products ON Products.id = Reviews.pid
WHERE uid = :uid
ORDER BY time_posted DESC
''', uid = uid)
        return [Review(*row) for row in rows]

    @staticmethod
    def update_review(id, newInput):
        rows = app.db.execute("""
UPDATE Reviews
SET review_text = :newInput, time_posted = current_timestamp AT TIME ZONE 'UTC'
WHERE id = :id
""",
                              id=id, newInput=newInput)
    @staticmethod
    def delete_review(id):
        rows = app.db.execute("""
DELETE FROM Reviews
WHERE id = :id
""",
                            id=id)
        return rows        
    @staticmethod 
    def get_all_by_pid(pid):
        rows = app.db.execute('''
SELECT Reviews.id, uid, pid, time_posted, rating, review_text, Products.name, Users.firstname
FROM Reviews
JOIN Products ON Products.id = Reviews.pid JOIN Users ON Reviews.uid = Users.id
WHERE pid = :pid
ORDER BY time_posted DESC
''', pid = pid)
        return [Review(*row) for row in rows]