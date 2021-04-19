from app.books.models import BookDetail
from flask import jsonify

POPULAR_BOOK_LIMIT_SIZE = 20


def get_all_books():
    books = BookDetail.query.all()
    json_list = BookDetail.to_json_many(books)

    result = jsonify(books=json_list)
    return result


def get_book(book_id):
    book = BookDetail.query.get(book_id)

    result = book.to_json()
    return result


def get_popular_books():
    popular_books = BookDetail \
        .query.order_by(BookDetail.popularity.desc()) \
        .limit(POPULAR_BOOK_LIMIT_SIZE)
    json_list = BookDetail.to_json_many(popular_books)

    result = jsonify(popular_books=json_list)
    return result
