import random

from flask import jsonify
from app import db
from sqlalchemy import desc


def get_all_members():
    members = Member.query.all()
    json_list = Member.to_json_many(members)

    result = jsonify(members=json_list)
    return result


def get_profitable_members():
    members = Member.query \
        .order_by(desc(Member.total_paid + Member.unbilled))
    json_list = Member.to_json_many(members)

    result = jsonify(members=json_list)
    return result


def get_member(member_id):
    # Handle edge cases [ invalid member_id ]
    if Member.query.get(member_id) is None:
        return jsonify(err_msg='invalid member_id')

    member = Member.query.get(member_id)
    json = member.to_json(calculate_unbilled=True)

    result = jsonify(member=json)
    return result


def create_member(username, email):
    member = Member()
    member.username = username
    member.email = email
    member.profile_pic = "https://i.pravatar.cc/150?img={}".format(random.randrange(0, 71))

    db.session.add(member)
    db.session.commit()

    json = member.to_json()
    result = jsonify(member=json)
    return result


def delete_member(member_id):
    if int(member_id) < 0:
        return jsonify(err_msg="invalid member_id")

    member = Member.query.get(member_id)
    if member is None:
        return jsonify(err_msg="member does not exist")

    member.delete_member()

    result = jsonify(msg="deleted member successfully")
    return result


def edit_member(member_id, username='', email=''):
    member = Member.query.get(member_id)
    member.edit_member(username, email)

    json = member.to_json()
    result = jsonify(member=json)
    return result


def search(key_word):
    members = Member.query.filter(Member.username.contains(key_word))
    return Member.to_json_many(members)


from app.users.models import Member
