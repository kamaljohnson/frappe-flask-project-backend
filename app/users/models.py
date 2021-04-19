from app import db


class User(db.Model):
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
        return '<Member {}>'.format(self.username)

    def to_json(self):
        json = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'unbilled': self.unbilled,
            'total_paid': self.total_paid,
            'transactions': Transaction.to_json_many(self.transactions)
        }
        return json

    @staticmethod
    def to_json_many(member_list):
        json_list = []
        for member in member_list:
            json_list.append(member.to_json())

        return json_list

    def calculate_unbilled(self):
        issued_transactions = Transaction.query \
            .filter_by(member_id=self.id) \
            .filter_by(returned=False)
        unbilled = 0
        for transaction in issued_transactions:
            unbilled += transaction.calculate_fees()
        self.unbilled = unbilled
        db.session.add(self)
        db.session.commit()

    def delete_member(self):
        db.session.delete(self)
        db.session.commit()

    def edit_member(self, username='', email=''):
        if username != '':
            self.username = username
        if email != '':
            self.email = email

        db.session.add(self)
        db.session.commit()


class Librarian(User):
    __tablename__ = 'librarian'

    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Librarian {}>'.format(User.query.get(self.user_id))

    def to_json(self):
        json = {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
        return json


from app.transactions.models import Transaction
