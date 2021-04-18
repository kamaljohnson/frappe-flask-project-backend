from app import db
from datetime import datetime, date
from app.books.models import BookDetail

"""
    the fine for each extra day after the due date
"""
EXTRA_PER_DAY_FINE = 10


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

    """
        calculate_fees(): calculates the dynamic fees
        new_fees = base_fees + EXTRA_PER_DAY_FINE * extra_days
    """

    def calculate_fees(self):
        self.fees = BookDetail.query.get(self.book_id).base_fees
        if self.due_date > datetime.utcnow():
            extra_days = (date.today() - self.due_date.date()).days
            self.fees += extra_days * EXTRA_PER_DAY_FINE

    # TODO:
    def issue_book(self, member_id, book_id):
        pass

    # TODO:
    def return_book(self, book_id):
        pass
