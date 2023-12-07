from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, address, balance):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.balance = balance

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, address, balance
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname, address):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname, address)
VALUES(:email, :password, :firstname, :lastname, :address)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname, address=address)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, address, balance
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None
    @staticmethod
    def update_email(id, newInput):
        rows = app.db.execute("""
UPDATE Users
SET email = :newInput
WHERE id = :id
""",
                              id=id, newInput=newInput)
    @staticmethod
    def update_firstName(id, newInput):
        rows = app.db.execute("""
UPDATE Users
SET firstname = :newInput
WHERE id = :id
""",
                              id=id, newInput=newInput)
    @staticmethod
    def update_lastName(id, newInput):
        rows = app.db.execute("""
UPDATE Users
SET lastname = :newInput
WHERE id = :id
""",
                              id=id, newInput=newInput)
    @staticmethod
    def update_address(id, newInput):
        rows = app.db.execute("""
UPDATE Users
SET address = :newInput
WHERE id = :id
""",
                              id=id, newInput=newInput)
    @staticmethod
    def update_balance(id, newInput):
        rows = app.db.execute("""
UPDATE Users
SET balance = :newInput 
WHERE id = :id
""",
                              id=id, newInput=newInput)
        
    @staticmethod
    def is_seller(id):
        rows = app.db.execute("""
SELECT *
FROM Seller
WHERE uid = :id
""",
                              id=id)
        
        return len(rows) > 0

