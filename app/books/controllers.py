from app.books.models import BookDetail, BookInstance
from flask import jsonify

POPULAR_BOOK_LIMIT_SIZE = 20


def get_all_books():
    books = BookDetail.query.all()
    result = jsonify({"Books": book.to_dict for book in books})

    return result


def get_popular_books():
    popular_books = BookDetail \
        .query.order_by(BookDetail.popularity.desc()) \
        .limit(POPULAR_BOOK_LIMIT_SIZE)
    result = jsonify({"Popular Books": book.to_dict for book in popular_books})

    return result
