from app import db
from sqlalchemy_serializer import SerializerMixin


class Report(db.Model, SerializerMixin):
    __tablename__ = 'report'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    books_issued = db.Column(db.Integer)
    earnings = db.Column(db.Integer)

    def __repr__(self):
        return '<Report date: {}, books_issued: {}, earnings: {} >'.format(self.date, self.books_issued, self.earnings)
