from app import db
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime, date
from app.books.models import BookDetail

"""
    the fine for each extra day after the due date
"""
EXTRA_PER_DAY_FINE = 10


class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    book_instance_id = db.Column(db.Integer, db.ForeignKey('book_instance.id'))
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    returned = db.Column(db.Boolean)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, default=None)
    return_date = db.Column(db.DateTime, default=None)
    fees = db.Column(db.Integer)

    def __repr__(self):
        return '<Transaction : {}, member_id: {}, returned: {}>'.format(self.name, self.author, self.description)

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
