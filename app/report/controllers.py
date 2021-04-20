from flask import jsonify


def get_all_reports():
    reports = Report.query.all()
    json_list = Report.to_json_many(reports)

    result = jsonify(reports=json_list)
    return result


def get_report(from_date, till_date):
    reports = Report.query\
        .filter(Report.date >= from_date)\
        .filter(Report.date <= till_date).all()
    if len(reports) <= 0:
        return jsonify(msg="Report not yet generated")

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


from app.report.models import Report
