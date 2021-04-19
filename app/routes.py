import json

from flask import request

from app import app, books, transactions

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
@app.route('/books/all')
def get_all_books():
    return books.controllers.get_all_books()


@app.route('/books/<book_id>')
def get_book(book_id):
    return books.controllers.get_book(book_id)


@app.route('/books/popular')
def get_popular_books():
    return books.controllers.get_popular_books()


@app.route('/books/issued/<member_id>')
def get_issued_books(member_id):
    return books.get_issued_books(member_id)


@app.route('/books/issued/all')
def get_all_issued_books():
    return books.controllers.get_all_issued_books()


# member apis
@app.route('/members/all')
def get_all_members():
    return "API UNDER CONSTRUCTION"


@app.route('/members/<member_id>/insight')
def get_member_insight(member_id):
    return "API UNDER CONSTRUCTION"


@app.route('/members/create_new')
def create_member():
    return "API UNDER CONSTRUCTION"


@app.route('/members/delete/<member_id>')
def delete_member(member_id):
    return "API UNDER CONSTRUCTION"


@app.route('/members/edit/<member_id>/')
def edit_member(member_id):
    return "API UNDER CONSTRUCTION"


@app.route('/library/insight')
def get_library_insight():
    return "API UNDER CONSTRUCTION"


# library apis
@app.route('/library/report')
def get_report():
    return "API UNDER CONSTRUCTION"


# transaction apis
@app.route('/transactions/all')
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
@app.route('/reports/all')
def get_all_report():
    return "API UNDER CONSTRUCTION"