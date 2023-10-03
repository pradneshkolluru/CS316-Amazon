from flask import current_app as app


class Wishes:
    def __init__(self, id, uid, pid, time_added):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_added = time_added

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_added
FROM Wishes
WHERE id = :id
''',
                              id=id)
        return Wishes(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, time_added
FROM Wishes
WHERE uid = :uid
AND time_added >= :since
ORDER BY time_added DESC
''',
                              uid=uid,
                              since=since)
        return [Wishes(*row) for row in rows]
    @staticmethod
    def add_item(uid, pid):
        try:
            rows = app.db.execute("""
INSERT INTO Wishes(uid, pid)
VALUES(:uid, :pid)
RETURNING id
""",
                                  uid=uid,
                                  pid=pid)
            id = rows[0][0]
            return Wishes.get(id)
        except Exception as e:
            # the following simply prints the error to the console:
            print(str(e))
            return None
