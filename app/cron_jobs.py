from app import app, scheduler


@scheduler.task('interval', id='calculate_member_unbilled', hours=24, misfire_grace_time=900)
def calculate_member_unbilled():
    """Calculates unbilled fees for the non-returned books"""
    members = Member.query.all()
    for member in members:
        member.calculate_unbilled()


@scheduler.task('interval', id='create_report', hours=24, misfire_grace_time=900)
def create_report():
    """Creates the report for the day"""
    report = Report()
    report.create_report()


from app.users.models import Member
from app.report.models import Report
