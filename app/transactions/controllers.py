from flask import jsonify
from .models import Transaction


def get_all_transactions():
    transactions = Transaction.query.all()

    result = jsonify(transactions=Transaction.to_json_many(transactions))
    return result


def issue_book(book_instance_id, member_id, issue_period):
    transaction = Transaction()
    issue_response = transaction.issue_book(book_instance_id, member_id, issue_period)

    if not issue_response["validity"]:
        result = jsonify(err_msg=issue_response["err_msg"])
    else:
        result = jsonify(transaction=transaction.to_json())

    return result


def return_book(book_instance_id):
    transaction = Transaction.query \
        .filter_by(book_instance_id=book_instance_id) \
        .filter_by(returned=False).first()

    if transaction is None:
        return jsonify(err_msg='book_instance not issued')

    transaction.return_book()

    result = jsonify(transaction=transaction.to_json())
    return result
