from app import db


class Report(db.Model):
    __tablename__ = 'report'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    books_issued = db.Column(db.Integer)
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