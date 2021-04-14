from app import app

"""
    Required routs
    
    - [GET] books/all
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


@app.route('/books/all')
def get_all_books():
    return "API UNDER CONSTRUCTION"


@app.route('/books/popular')
def get_popular_books():
    return "API UNDER CONSTRUCTION"


@app.route('/books/issued/<member_id>')
def get_issued_books(member_id):
    return "API UNDER CONSTRUCTION"


@app.route('/books/issued/all')
def get_all_issued_books():
    return "API UNDER CONSTRUCTION"


@app.route('/members/<member_id>/insight')
def get_member_insight(member_id):
    return "API UNDER CONSTRUCTION"


@app.route('/insight')
def get_library_insight():
    return "API UNDER CONSTRUCTION"


@app.route('/report')
def get_report():
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


@app.route('/transactions/issue_book')
def issue_book():
    return "API UNDER CONSTRUCTION"


@app.route('/transactions/return_book')
def return_book():
    return "API UNDER CONSTRUCTION"


