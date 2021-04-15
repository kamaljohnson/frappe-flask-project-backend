from app import db
from sqlalchemy_serializer import SerializerMixin


class BookDetail(db.Model, SerializerMixin):
    __tablename__ = 'book_detail'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    description = db.Column(db.String(500))
    author = db.Column(db.String(20))
    base_fees = db.Column(db.Integer)
    popularity = db.Column(db.Integer, index=True)
    stock = db.Column(db.Integer)  # is updated when a book is issued / returned

    # back populates
    book_instances = db.relationship('BookInstance', back_populates='book_detail')

    def __repr__(self):
        return '<Book name: {}, author: {}, description: {} >'.format(self.name, self.author, self.description)

    # TODO:
    def get_book_stock(self):
        pass


class BookInstance(db.Model, SerializerMixin):
    __tablename__ = 'book_instance'

    id = db.Column(db.Integer, primary_key=True)
    is_available = db.Column(db.Boolean)

    # foreign keys
    book_detail_id = db.Column(db.Integer, db.ForeignKey('book_detail.id'))

    # back populates
    book_detail = db.relationship('BookDetail', back_populates='book_instances')
    transactions = db.relationship('Transaction', back_populates='book_instance')

    """
    available: is the book available at the library,
    or is it issued to a member
    
    transactions: all the issues/returns made by different
    members with this book entity
    """

    def __repr__(self):
        return '<Book name: {}, quantity: {}>'.format(BookDetail.query.get(self.book_detail_id).name, self.quantity_left)
