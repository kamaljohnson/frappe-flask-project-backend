from app import db
from sqlalchemy_serializer import SerializerMixin


class User(db.Model, SerializerMixin):
    __abstract__ = True

    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(200), unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Member(User):
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True)
    unbilled = db.Column(db.Integer)
    total_paid = db.Column(db.Integer)

    # back populates
    transactions = db.relationship('Transaction', back_populates='member')

    """
        transactions: use to retrieve all the books issued/returned and details
            - issued: transactions for t.returned = false
    """

    def __repr__(self):
        return '<Member {}>'.format(User.query.get(self.user_id))

    # TODO:
    def calculate_unbilled(self):
        pass

    # TODO:
    def update_total_paid(self, amount):
        pass


class Librarian(User):
    __tablename__ = 'librarian'

    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Librarian {}>'.format(User.query.get(self.user_id))
