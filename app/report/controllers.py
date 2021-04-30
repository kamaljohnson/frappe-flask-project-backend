from flask import jsonify
from sqlalchemy import desc


def get_all_reports(limited=False, days=-1):
    if not limited:
        reports = Report.query.order_by(desc(Report.date)).all()
    else:
        if days < 0:
            return jsonify(msg="invalid days input")
        reports = Report.query.order_by(desc(Report.date)).limit(days)

    json_list = Report.to_json_many(reports)

    result = jsonify(reports=json_list)
    return result


def get_report(from_date, till_date):
    reports = Report.query \
        .filter(Report.date >= from_date) \
        .filter(Report.date <= till_date).all()
    if len(reports) <= 0:
        return jsonify(msg="report not generated")

    earnings = 0
    books_issued = 0
    books_returned = 0

    for report in reports:
        earnings += report.earnings
        books_issued += report.books_issued
        books_returned += report.books_returned

    result = jsonify(report={
        'from_date': from_date,
        'till_date': till_date,
        'earnings': earnings,
        'books_issued': books_returned,
        'books_returned': books_returned
    })
    return result


def get_library_insight():
    total_books = len(BookInstance.query.all())
    members = len(Member.query.all())
    books_issued = 0
    total_earnings = 0

    reports = Report.query.all()
    for report in reports:
        total_earnings += report.earnings
        books_issued += report.books_issued

    result = jsonify(insight={
        'total_books': total_books,
        'books_issued': books_issued,
        'members': members,
        'total_earnings': total_earnings
    })
    return result


from app.report.models import Report
from app.books.models import BookInstance
from app.users.models import Member
