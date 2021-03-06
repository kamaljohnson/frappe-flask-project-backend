import datetime
import json
from flask_cors import cross_origin
from flask import request, jsonify

from app import app, books, transactions, users, report


# books apis
@app.route('/books/all', methods=['GET'])
@cross_origin()
def get_all_books():
    return books.controllers.get_all_books()


@app.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    return books.controllers.get_book(book_id)


@app.route('/books/instances/<book_instance_id>', methods=['GET'])
def get_book_instance(book_instance_id):
    return books.controllers.get_book_instance(book_instance_id)


@app.route('/books/popular', methods=['GET'])
def get_popular_books():
    return books.controllers.get_popular_books()


@app.route('/books/issued/<member_id>', methods=['GET'])
def get_issued_books(member_id):
    return books.get_issued_books(member_id)


@app.route('/books/issued/all', methods=['GET'])
def get_all_issued_books():
    return books.controllers.get_all_issued_books()


@app.route('/books/issued/limit/<limit>', methods=['GET'])
def get_limit_issued_books(limit):
    return books.controllers.get_limit_issued_books(limit)


@app.route('/books/create/', methods=['POST'])
def create_book():
    book_detail = json.loads(request.data)

    name = book_detail['name']
    author = book_detail['author']
    description = book_detail['description']
    base_fees = book_detail['base_fees']

    return books.controllers.create_book(
        name=name,
        author=author,
        description=description,
        base_fees=base_fees
    )


@app.route('/books/edit/<book_id>', methods=['POST'])
def update_book(book_id):
    book_detail = json.loads(request.data)

    name = book_detail['name']
    author = book_detail['author']
    description = book_detail['description']
    base_fees = book_detail['base_fees']

    return books.controllers.update_book(
        book_id=book_id,
        name=name,
        author=author,
        description=description,
        base_fees=base_fees
    )


@app.route('/books/delete/<book_id>', methods=['GET'])
def delete_book(book_id):
    return books.controllers.delete_book(book_id)


@app.route('/books/add/<book_id>', methods=['GET'])
def add_book_instance(book_id):
    return books.controllers.add_book_instance(book_id)


# member apis
@app.route('/members/all', methods=['GET'])
def get_all_members():
    return users.controllers.get_all_members()


@app.route('/members/profitable', methods=['GET'])
def get_profitable_members():
    return users.controllers.get_profitable_members()


@app.route('/members/<member_id>', methods=['GET'])
def get_member(member_id):
    return users.controllers.get_member(member_id)


@app.route('/members/create', methods=['POST'])
def create_member():
    member_details = json.loads(request.data)

    if 'username' not in member_details or \
            'email' not in member_details:
        return jsonify(err_msg='insufficient info')

    if type(member_details['username']) != str or \
            type(member_details['email']) != str:
        return jsonify(err_msg='invalid info type')

    if member_details['username'] == '' or \
            member_details['email'] == '':
        return jsonify(err_msg='invalid member info')

    username = member_details['username']
    email = member_details['email']

    return users.controllers.create_member(username, email)


@app.route('/members/delete/<member_id>')
def delete_member(member_id):
    return users.controllers.delete_member(member_id)


@app.route('/members/edit/<member_id>', methods=['POST'])
def edit_member(member_id):
    edit_details = json.loads(request.data)

    if 'username' not in edit_details:
        new_username = ''
    else:
        new_username = edit_details['username']

    if 'email' not in edit_details:
        new_email = ''
    else:
        new_email = edit_details['email']

    if type(new_username) != str or \
            type(new_email) != str:
        return jsonify(err_msg="invalid type")

    if new_username == '' and \
            new_email == '':
        return jsonify(err_msg="empty fields")

    return users.controllers.edit_member(member_id, new_username, new_email)


@app.route('/members/<member_id>/insight', methods=['GET'])
def get_member_insight(member_id):
    pass


# search
@app.route('/search', methods=['POST'])
def get_search_results():
    search_details = json.loads(request.data)

    if 'search_word' not in search_details or \
            'filters' not in search_details:
        return jsonify(err_msg='empty fields')

    key_word = search_details['search_word']
    filters = search_details['filters']

    result = {}

    if filters['books']:
        result['books'] = books.controllers.search(key_word)

    if filters['members']:
        result['members'] = users.controllers.search(key_word)

    return jsonify(result=result)


# transaction apis
@app.route('/transactions/all', methods=['GET'])
def get_all_transactions():
    return transactions.controllers.get_all_transactions()


@app.route('/transactions/issue_book', methods=['POST'])
def issue_book():
    issue_details = json.loads(request.data)

    if 'book_instance_id' not in issue_details or \
            'member_id' not in issue_details or \
            'issue_period' not in issue_details:
        return jsonify(err_msg='empty fields')

    book_instance_id = issue_details['book_instance_id']
    member_id = issue_details['member_id']
    issue_period = issue_details['issue_period']

    return transactions.controllers.issue_book(book_instance_id, member_id, issue_period)


@app.route('/transactions/return_book/<book_instance_id>', methods=['GET'])
def return_book(book_instance_id):
    return transactions.controllers.return_book(book_instance_id)


# analytics apis
@app.route('/library/reports/all/<days>', methods=['GET'])
def get_all_reports_days(days):
    days = int(days)
    return report.controllers.get_all_reports(limited=True, days=days)


@app.route('/library/reports/all/', methods=['GET'])
def get_all_reports():
    return report.controllers.get_all_reports()


@app.route('/library/report', methods=['GET'])
def get_report():
    request_details = json.loads(request.data)

    if 'from_date' not in request_details or \
            'till_date' not in request_details:
        return jsonify(err_msg='empty fields')

    from_date_str = request_details['from_date']
    till_date_str = request_details['till_date']

    from_date = datetime.datetime.strptime(from_date_str, "%Y-%m-%d").date()
    till_date = datetime.datetime.strptime(till_date_str, "%Y-%m-%d").date()
    return report.get_report(from_date, till_date)


@app.route('/library/insight', methods=['GET'])
def get_library_insight():
    return report.get_library_insight()
