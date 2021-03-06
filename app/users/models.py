from app import db


class User(db.Model):
    __abstract__ = True

    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(200), unique=True)
    profile_pic = db.Column(db.String(200))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Member(User):
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True)
    unbilled = db.Column(db.Integer, default=0)
    total_paid = db.Column(db.Integer, default=0)
    books_taken = db.Column(db.Integer, default=0)

    # back populates
    transactions = db.relationship('Transaction', back_populates='member')

    """
        transactions: use to retrieve all the books issued/returned and details
            - issued: transactions for t.returned = false
    """

    def __repr__(self):
        return '<Member {}>'.format(self.username)

    def to_json(self, calculate_unbilled=False):
        calculate_fees = False

        if calculate_unbilled:
            self.calculate_unbilled()
            calculate_fees = True

        json = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'profile_pic': self.profile_pic,
            'unbilled': self.unbilled,
            'total_paid': self.total_paid,
            'books_taken': self.books_taken,
            'transactions': Transaction.to_json_many(self.transactions, calculate_fees)
        }
        return json

    @staticmethod
    def to_json_many(member_list, calculate_unbilled=False):
        json_list = []
        for member in member_list:
            json_list.append(member.to_json(calculate_unbilled))

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
