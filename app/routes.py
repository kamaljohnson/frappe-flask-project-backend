import datetime
import json

from flask import request

from app import app, books, transactions, users, report

"""
    Required routs
    
    - [GET] books/all
    - [GET] books/<book_id>
    - [GET] books/popular
    - [GET] books/issued/<member_id>
    - [GET] books/issued/all
    
    - [GET] members/popular
    
    - [GET] member/<member_id>/insight
    - [GET] /insight                        :library insight
    
    - [GET] report/                         :start_data till end_date
                                             specified in api call
    
    - [POST] members/create_new
    - [POST] members/delete/<member_id>
    - [POST] members/edit/<member_id>
    
    - [POST] transaction/issue_book
    - [POST] transaction/return_book
"""


# books apis
@app.route('/books/all', methods=['GET'])
def get_all_books():
    return books.controllers.get_all_books()


@app.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    return books.controllers.get_book(book_id)


@app.route('/books/popular', methods=['GET'])
def get_popular_books():
    return books.controllers.get_popular_books()


@app.route('/books/issued/<member_id>', methods=['GET'])
def get_issued_books(member_id):
    return books.get_issued_books(member_id)


@app.route('/books/issued/all', methods=['GET'])
def get_all_issued_books():
    return books.controllers.get_all_issued_books()


# member apis
@app.route('/members/all', methods=['GET'])
def get_all_members():
    return users.controllers.get_all_members()


@app.route('/member/<member_id>', methods=['GET'])
def get_member(member_id):
    return users.controllers.get_member(member_id)


@app.route('/members/create_new', methods=['POST'])
def create_member():
    member_details = json.loads(request.data)

    username = member_details['username']
    email = member_details['email']

    return users.controllers.create_member(username, email)


@app.route('/members/delete/<member_id>')
def delete_member(member_id):
    return users.controllers.delete_member(member_id)


@app.route('/members/edit/<member_id>/', methods=['POST'])
def edit_member(member_id):
    edit_details = json.loads(request.data)

    new_username = edit_details['username']
    new_email = edit_details['email']

    if new_username is None:
        new_username = ''
    if new_email is None:
        new_email = ''

    return users.controllers.edit_member(member_id, new_username, new_email)


@app.route('/library/insight', methods=['GET'])
def get_library_insight():
    return "API UNDER CONSTRUCTION"


# transaction apis
@app.route('/transactions/all', methods=['GET'])
def get_all_transactions():
    return transactions.controllers.get_all_transactions()


@app.route('/transactions/issue_book', methods=['POST'])
def issue_book():
    issue_details = json.loads(request.data)

    book_instance_id = issue_details['book_instance_id']
    member_id = issue_details['member_id']
    issue_period = issue_details['issue_period']

    return transactions.controllers.issue_book(book_instance_id, member_id, issue_period)


@app.route('/transactions/return_book/<book_instance_id>', methods=['GET'])
def return_book(book_instance_id):
    return transactions.controllers.return_book(book_instance_id)


# analytics apis
@app.route('/library/reports/all', methods=['GET'])
def get_all_reports():
    return report.controllers.get_all_reports()


@app.route('/library/report', methods=['GET'])
def get_report():
    body = json.loads(request.data)

    from_date_str = body['from_date']
    till_date_str = body['till_date']

    from_date = datetime.datetime.strptime(from_date_str, "%Y-%m-%d").date()
    till_date = datetime.datetime.strptime(till_date_str, "%Y-%m-%d").date()
    return report.get_report(from_date, till_date)
