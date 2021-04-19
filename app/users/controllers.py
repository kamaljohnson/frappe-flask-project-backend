from flask import jsonify
from app import db


def get_all_members():
    members = Member.query.all()
    json_list = Member.to_json_many(members)

    result = jsonify(members=json_list)
    return result


def create_member(username, email):
    member = Member()
    member.username = username
    member.email = email

    db.session.add(member)
    db.session.commit()

    json = member.to_json()
    result = jsonify(member=json)
    return result


def delete_member(member_id):
    member = Member.query.get(member_id)
    member.delete_member()

    result = jsonify(msg="deleted member successfully")
    return result


def edit_member(member_id, username='', email=''):
    member = Member.query.get(member_id)
    member.edit_member(username, email)

    json = member.to_json()
    result = jsonify(member=json)
    return result


def get_member_insight(member_id):
    pass


def get_library_insight():
    pass


from app.users.models import Member
