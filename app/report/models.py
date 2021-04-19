from app import db
from datetime import datetime


class Report(db.Model):
    __tablename__ = 'report'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    books_issued = db.Column(db.Integer)
    books_returned = db.Column(db.Integer)
    earnings = db.Column(db.Integer)

    def __repr__(self):
        return '<Report date: {}, books_issued: {}, earnings: {} >'.format(self.date, self.books_issued, self.earnings)

    def to_json(self):
        json = {
            'id': self.id,
            'date': self.date,
            'books_issued': self.books_issued,
            'earnings': self.earnings
        }
        return json

    @staticmethod
    def to_json_many(report_list):
        json_list = []
        for report in report_list:
            json_list.append(report.to_json())

        return json_list

    def create_report(self, date=datetime.today()):
        self.date = date
        self.books_issued = 0
        self.earnings = 0
        # get books issued on the date
        issued_transactions = Transaction.query.filter_by(issue_date=date).all()
        self.books_issued = len(issued_transactions)
        # get earnings for today
        returned_transactions = Transaction.query.filter_by(return_date=date).all()
        self.books_returned = len(returned_transactions)
        for transaction in returned_transactions:
            self.earnings += transaction.fees

        db.session.add(self)
        db.session.commit()


from app.transactions.models import Transaction
