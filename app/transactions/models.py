from app import db
from datetime import datetime, timedelta

"""
    the fine for each extra day after the due date
"""
EXTRA_PER_DAY_FINE = 2


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    returned = db.Column(db.Boolean)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, default=None)
    return_date = db.Column(db.DateTime, default=None)
    fees = db.Column(db.Integer)

    # foreign keys
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    book_instance_id = db.Column(db.Integer, db.ForeignKey('book_instance.id'))

    # back populates
    book_instance = db.relationship('BookInstance', back_populates='transactions')
    member = db.relationship('Member', back_populates='transactions')

    def __repr__(self):
        return '<Transaction : {}, member_id: {}, returned: {}>'.format(self.name, self.author, self.description)

    def to_json(self):
        json = {
            'id': self.id,
            'returned': self.returned,
            'issue_date': self.issue_date,
            'due_date': self.due_date,
            'return_date': self.return_date,
            'fees': self.fees,
            'member_id': self.member_id,
            'book_instance_id': self.book_instance_id
        }
        return json

    @staticmethod
    def to_json_many(transaction_list):
        json_list = []
        for transaction in transaction_list:
            json_list.append(transaction.to_json())

        return json_list

    """
        calculate_fees(): calculates the dynamic fees
        new_fees = base_fees + EXTRA_PER_DAY_FINE * extra_days
    """

    def calculate_fees(self):
        self.fees = BookDetail.query.get(self.book_instance.book_detail_id).base_fees
        if not self.returned:
            period = (datetime.utcnow() - self.issue_date).days
        else:
            period = (self.return_date - self.issue_date).days

        if self.issue_date + timedelta(days=period) > self.due_date:
            extra_days = period - (self.issue_date.date() - self.due_date.date()).days
            self.fees += extra_days * EXTRA_PER_DAY_FINE

        db.session.add(self)
        db.session.commit()

        if not self.returned:
            return self.fees

    def issue_book(self, book_instance_id, member_id, issue_period, issue_date=datetime.utcnow()):
        # Doing checks to find if issue transaction is valid or not
        # 1: parameter logic check
        book_instance = BookInstance.query.get(book_instance_id)
        member = Member.query.get(member_id)

        if book_instance is None:
            return {"VALIDITY": False, "ERROR_MSG": "Invalid book_instance_id, no such book_instance exist in database"}
        if member is None:
            return {"VALIDITY": False, "ERROR_MSG": "Invalid member_id, no such member exist in database"}
        if issue_period <= 0:
            return {"VALIDITY": False, "ERROR_MSG": "Invalid issue period, issue_period must be a non negative integer"}
        if issue_date > datetime.utcnow():
            return {"VALIDITY": False, "ERROR_MSG": "Invalid issue_date, issue_date must not be a future date"}

        # 2: check if book_instance is available
        if not book_instance.is_available:
            return {"VALIDITY": False, "ERROR_MSG": "Book Unavailable, the book instance is already issued to a member"}

        # 3: check if member unbilled < 500
        if member.unbilled >= 500:
            return {"VALIDITY": False, "ERROR_MSG": "Member max debt reached, member requires to return the books in order to issue new ones"}

        self.returned = False
        self.member = member
        self.book_instance = book_instance
        self.issue_date = issue_date
        self.due_date = self.issue_date + timedelta(days=issue_period)

        self.book_instance.is_available = False

        db.session.add(self)
        db.session.commit()

        book_detail = BookDetail.query.get(self.book_instance.book_detail_id)
        book_detail.update_stock(-1)

        return {"VALIDITY": True}

    def return_book(self, return_date=datetime.utcnow()):
        self.returned = True
        self.return_date = return_date
        self.calculate_fees()

        self.book_instance.is_available = True
        self.member.unbilled = 0

        db.session.add(self)
        db.session.commit()

        book_detail = BookDetail.query.get(self.book_instance.book_detail_id)
        book_detail.update_popularity(self.fees)
        book_detail.update_stock(1)


from app.books.models import BookDetail, BookInstance
from app.users.models import Member
