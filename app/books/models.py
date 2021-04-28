from app import db


class BookDetail(db.Model):
    __tablename__ = 'book_detail'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    description = db.Column(db.String(500), nullable=False)
    author = db.Column(db.String(20), nullable=False)
    img_src = db.Column(db.String(120))
    base_fees = db.Column(db.Integer, nullable=False)
    popularity = db.Column(db.Integer, index=True, default=0)
    stock = db.Column(db.Integer, default=0)  # is updated when a book is issued / returned

    # back populates
    book_instances = db.relationship('BookInstance', back_populates='book_detail')

    def __repr__(self):
        return '<Book name: {}, author: {}, description: {} >'.format(self.name, self.author, self.description)

    def to_json(self, simple=True):
        json = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'author': self.author,
            'img_src': self.img_src,
            'base_fees': self.base_fees,
            'popularity': self.popularity,
            'stock': self.stock,
        }
        if not simple:
            json['book_instances'] = BookInstance.to_json_many(self.book_instances)

        return json

    @staticmethod
    def to_json_many(book_list, simple=True):
        json_list = []
        for book in book_list:
            json_list.append(book.to_json(simple))

        return json_list

    def update_stock(self, update_count):
        self.stock += update_count
        db.session.add(self)
        db.session.commit()

    def update_popularity(self, collected_fees):
        self.popularity += collected_fees
        db.session.add(self)
        db.session.commit()


class BookInstance(db.Model):
    __tablename__ = 'book_instance'

    id = db.Column(db.Integer, primary_key=True)
    is_available = db.Column(db.Boolean, default=True)

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
        return '<Book name: {}>'.format(BookDetail.query.get(self.book_detail_id).name)

    def to_json(self, simple=True):
        json = {
            'id': self.id,
            'is_available': self.is_available,
            'book_detail_id': self.book_detail_id,
            'transactions': Transaction.to_json_many(self.transactions)
        }
        if not simple:
            json['book_detail'] = self.book_detail.to_json(simple=True)

        return json

    @staticmethod
    def to_json_many(book_instance_list, simple=True):
        json_list = []
        for book in book_instance_list:
            json_list.append(book.to_json(simple))

        return json_list

    @staticmethod
    def create_new(book_detail_id):
        book_instance = BookInstance()
        book_instance.book_detail_id = book_detail_id
        db.session.add(book_instance)
        db.session.commit()

        book_detail = BookDetail.query.get(book_detail_id)
        book_detail.update_stock(1)


from app.transactions.models import Transaction
