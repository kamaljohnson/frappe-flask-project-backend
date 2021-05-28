from flask import jsonify
from sqlalchemy import desc

POPULAR_BOOK_LIMIT_SIZE = 20


def get_all_books():
    books = BookDetail.query.all()
    json_list = BookDetail.to_json_many(books, simple=False)

    result = jsonify(books=json_list)
    return result


def get_book(book_id):
    if int(book_id) < 0:
        return jsonify(err_msg="invalid book_id")
    if BookDetail.query.get(book_id) is None:
        return jsonify(err_msg='book does not exist')

    book = BookDetail.query.get(book_id)

    json = book.to_json()
    result = jsonify(book=json)
    return result


def get_book_instance(book_instance_id):
    if int(book_instance_id) < 0:
        return jsonify(err_msg="invalid book_id")
    if BookInstance.query.get(book_instance_id) is None:
        return jsonify(err_msg='book instance does not exist')

    book = BookInstance.query.get(book_instance_id)

    json = book.to_json(simple=False)
    result = jsonify(book_instance=json)
    return result


def get_popular_books():
    popular_books = BookDetail \
        .query.order_by(BookDetail.popularity.desc()) \
        .limit(POPULAR_BOOK_LIMIT_SIZE)
    json_list = BookDetail.to_json_many(popular_books)

    result = jsonify(popular_books=json_list)
    return result


def get_all_issued_books():
    issued_transactions = app.transactions.models.Transaction.query \
        .filter_by(returned=False) \
        .order_by(desc(app.transactions.models.Transaction.issue_date))

    issued_books = []

    for transaction in issued_transactions:
        issued_book = transaction.book_instance
        issued_books.append(issued_book)

    result = jsonify(issued_books=BookInstance.to_json_many(issued_books, simple=False))
    return result


def get_limit_issued_books(limit):
    issued_transactions = app.transactions.models.Transaction.query \
        .filter_by(returned=False) \
        .order_by(desc(app.transactions.models.Transaction.issue_date)) \
        .limit(limit)

    issued_books = []

    for transaction in issued_transactions:
        issued_book = transaction.book_instance
        issued_books.append(issued_book)

    result = jsonify(issued_books=BookInstance.to_json_many(issued_books, simple=False))
    return result


def get_issued_books(member_id):
    if Member.query.get(member_id) is None:
        return jsonify(err_msg='invalid member_id')

    issued_transactions = app.transactions.models.Transaction.query \
        .filter_by(member_id=member_id) \
        .filter_by(returned=False)
    issued_books = []

    for transaction in issued_transactions:
        issued_book = transaction.book_instance
        issued_books.append(issued_book)

    result = jsonify(issued_books=BookInstance.to_json_many(issued_books))
    return result


def create_book(name, author, description, base_fees):
    new_book = BookDetail()
    new_book.name = name
    new_book.author = author
    new_book.description = description
    new_book.base_fees = base_fees

    db.session.add(new_book)
    db.session.commit()

    result = jsonify(book_detail=new_book.to_json())
    return result


def update_book(book_id, name, author, description, base_fees):
    book = BookDetail.query.get(book_id)
    book.name = name
    book.author = author
    book.description = description
    book.base_fees = base_fees

    db.session.add(book)
    db.session.commit()

    result = jsonify(book_detail=book.to_json())
    return result


def delete_book(book_id):
    book = BookDetail.query.get(book_id)

    book.delete_book()

    result = jsonify(msg='deleted book successfully')
    return result


def add_book_instance(book_id):
    book_instance = BookInstance.create_new(book_id)

    result = jsonify(book_instance=book_instance.to_json())
    return result


def search(key_word) -> object:
    books = BookDetail.query.filter(BookDetail.name.contains(key_word))
    return BookDetail.to_json_many(books)


import app.transactions.models
from app.books.models import BookDetail, BookInstance
from app.users.models import Member
from app import db
