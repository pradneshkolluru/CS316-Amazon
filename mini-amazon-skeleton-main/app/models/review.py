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
SELECT Reviews.id, uid, pid, time_posted, rating, review_text, name, '' firstname
FROM Reviews
JOIN Products ON Products.id = Reviews.pid
WHERE uid = :uid
ORDER BY time_posted DESC
''', uid = uid)
        return [Review(*row) for row in rows]
    @staticmethod
    def update_review(id, newInput, newInputRating):
        rows = app.db.execute("""
UPDATE Reviews
SET review_text = :newInput, time_posted = current_timestamp AT TIME ZONE 'EST', rating = :newInputRating
WHERE id = :id
""",
                              id=id, newInput=newInput,newInputRating=newInputRating)

#     @staticmethod
#     def update_review(id, newInput):
#         rows = app.db.execute("""
# UPDATE Reviews
# SET review_text = :newInput, time_posted = current_timestamp AT TIME ZONE 'UTC'
# WHERE id = :id
# """,
#                               id=id, newInput=newInput)
#     @staticmethod
#     def update_rating(id, newInput):
#         rows = app.db.execute("""
# UPDATE Reviews
# SET rating = :newInput, time_posted = current_timestamp AT TIME ZONE 'UTC'
# WHERE id = :id
# """,
#                               id=id, newInput=newInput)    
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
    
    @staticmethod
    def add_review(uid, pid, time_posted, rating, review_text):
        
        # try:
            rows = app.db.execute("""
INSERT INTO Reviews(uid, pid, time_posted, rating, review_text)
VALUES(:uid, :pid, :time_posted, :rating, :review_text)                      
""",
                                  uid=uid,
                                  pid=pid,
                                  time_posted=time_posted, rating=rating, review_text=review_text)
            # id = rows[0][0]
            return rows if rows else None
        # except Exception as e:
        #     # likely email already in use; better error checking and reporting needed;
        #     # the following simply prints the error to the console:
        #     print(str(e))
        #     return None
    @staticmethod
    def review_exists(uid, pid):
        rows = app.db.execute("""
SELECT *
FROM Reviews
WHERE uid = :uid AND pid =:pid
""",
                              uid=uid, pid=pid)
        return len(rows) > 0