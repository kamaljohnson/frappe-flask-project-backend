from flask import jsonify


def get_all_reports():
    reports = Report.query.all()
    json_list = Report.to_json_many(reports)

    result = jsonify(reports=json_list)
    return result


def get_report(date):
    reports = Report.query.filter_by(date=date).all()
    if len(reports) <= 0:
        return jsonify(msg="Report not yet generated")
    else:
        report = reports[0]

    json = report.to_json()

    result = jsonify(report=json)
    return result


from app.report.models import Report
