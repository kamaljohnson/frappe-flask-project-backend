from app import app, scheduler


@scheduler.task('interval', id='calculate_member_unbilled', hours=24, misfire_grace_time=900)
def calculate_member_unbilled():
    """Calculates unbilled fees for the non-returned books"""
    members = Member.query.all()
    for member in members:
        member.calculate_unbilled()
        print("Member: ", member.username, " Unbilled : ", member.unbilled)


from app.users.models import Member