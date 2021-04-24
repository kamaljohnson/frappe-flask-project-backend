from datetime import datetime, timedelta
import json
import random
import unittest

from app import app
from app import dummy_data_creator, db

DUMMY_DATA_SIZE = "small"


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        dummy_data_creator.add_dummy_data(DUMMY_DATA_SIZE, show_print=False)

    def test_get_all_books(self):
        # When
        response = self.app.get('/books/all')

        # Then
        self.assertEqual(dummy_data_creator.SAMPLE_UNIQUE_BOOK_SIZE[DUMMY_DATA_SIZE], len(response.json['books']))
        self.assertEqual(int, type(response.json['books'][0]['id']))

    def test_get_book(self):
        # When
        book_id = random.randrange(1, dummy_data_creator.SAMPLE_UNIQUE_BOOK_SIZE[DUMMY_DATA_SIZE] + 1)
        response = self.app.get('/books/{}'.format(book_id))

        # Then
        self.assertEqual(BookDetail.query.get(book_id).id, response.json['book']['id'])

        # When
        book_id = -1
        response = self.app.get('books/{}'.format(book_id))

        # Then
        self.assertEqual('invalid book_id', response.json['err_msg'])

        # When
        book_id = dummy_data_creator.SAMPLE_UNIQUE_BOOK_SIZE[DUMMY_DATA_SIZE] + 1
        response = self.app.get('books/{}'.format(book_id))

        # Then
        self.assertEqual('book does not exist', response.json['err_msg'])

    def test_get_popular_books(self):
        # When
        response = self.app.get('/books/popular')

        # Then
        self.assertEqual(int, type(response.json['popular_books'][0]['id']))

    def test_get_issued_books(self):
        # When
        member_id = random.randrange(1, dummy_data_creator.SAMPLE_MEMBER_SIZE[DUMMY_DATA_SIZE] + 1)
        response = self.app.get('/books/issued/{}'.format(member_id))

        # Then
        issued_books = response.json['issued_books']
        if len(issued_books) > 0:
            self.assertEqual(int, type(issued_books[0]['id']))

        # When
        member_id = -1  # invalid member_id
        response = self.app.get('/books/issued/{}'.format(member_id))

        # Then
        self.assertEqual('invalid member_id', response.json['err_msg'])

        # When
        member_id = dummy_data_creator.SAMPLE_MEMBER_SIZE[DUMMY_DATA_SIZE] + 1  # invalid member_id
        response = self.app.get('/books/issued/{}'.format(member_id))

        # Then
        self.assertEqual('invalid member_id', response.json['err_msg'])

    def test_get_all_issued_books(self):
        # When
        response = self.app.get('/books/issued/all')

        # Then
        if len(response.json['issued_books']) > 0:
            self.assertEqual(int, type(response.json['issued_books'][0]['id']))

    def test_get_all_members(self):
        # When
        response = self.app.get('/members/all')

        # Then
        self.assertEqual(dummy_data_creator.SAMPLE_MEMBER_SIZE[DUMMY_DATA_SIZE], len(response.json['members']))
        if len(response.json['members']) > 0:
            self.assertEqual(int, type(response.json['members'][0]['id']))

    def test_get_member(self):
        # When
        member_id = random.randrange(1, dummy_data_creator.SAMPLE_MEMBER_SIZE[DUMMY_DATA_SIZE] + 1)
        response = self.app.get('members/{}'.format(member_id))

        # Then
        member = response.json['member']
        self.assertEqual(member_id, member['id'])

        # When
        member_id = -1
        response = self.app.get('members/{}'.format(member_id))

        # Then
        self.assertEqual('invalid member_id', response.json['err_msg'])

        # When
        member_id = dummy_data_creator.SAMPLE_MEMBER_SIZE[DUMMY_DATA_SIZE] + 1
        response = self.app.get('members/{}'.format(member_id))

        # Then
        self.assertEqual('invalid member_id', response.json['err_msg'])

    def test_create_member(self):
        # When
        members_count_old = len(Member.query.all())
        payload = json.dumps({
            'username': 'test-username-1',
            'email': 'test-email-1'
        })
        resource = self.app.post('members/create', data=payload)

        # Then
        members_count_new = len(Member.query.all())
        self.assertEqual(int, type(resource.json['member']['id']))
        self.assertEqual(members_count_old + 1, members_count_new)

        # When
        payload = json.dumps({  # invalid member info
            'username': '',
            'email': ''
        })
        resource = self.app.post('members/create', data=payload)

        # Then
        self.assertEqual('invalid member info', resource.json['err_msg'])

        payload = json.dumps({  # insufficient info

        })
        resource = self.app.post('members/create', data=payload)

        # Then
        self.assertEqual('insufficient info', resource.json['err_msg'])

        # When
        payload = json.dumps({  # invalid info type
            'username': 1234,
            'email': 1234
        })
        resource = self.app.post('members/create', data=payload)

        # Then
        self.assertEqual('invalid info type', resource.json['err_msg'])

    def test_delete_member(self):
        # When
        member_id = Member.query.get(random.randrange(1, dummy_data_creator.SAMPLE_MEMBER_SIZE[DUMMY_DATA_SIZE] + 1)).id
        members_count_old = len(Member.query.all())
        resource = self.app.get('members/delete/{}'.format(member_id))

        # Then
        members_count_new = len(Member.query.all())
        self.assertEqual("deleted member successfully", resource.json['msg'])
        self.assertEqual(members_count_old - 1, members_count_new)

        # When
        member_id = dummy_data_creator.SAMPLE_MEMBER_SIZE[DUMMY_DATA_SIZE] + 1  # member does not exist
        resource = self.app.get('members/delete/{}'.format(member_id))

        # Then
        self.assertEqual("member does not exist", resource.json['err_msg'])

        # When
        member_id = -1
        resource = self.app.get('members/delete/{}'.format(member_id))

        # Then
        self.assertEqual("invalid member_id", resource.json['err_msg'])

    def test_edit_member(self):
        # When
        member_id = Member.query.get(random.randrange(1, dummy_data_creator.SAMPLE_MEMBER_SIZE[DUMMY_DATA_SIZE] + 1)).id
        payload = json.dumps({
            'username': 'test-username-1',
            'email': 'test-email-1'
        })
        resource = self.app.post('members/edit/{}'.format(member_id), data=payload)

        # Then
        self.assertEqual("test-username-1", resource.json['member']['username'])
        self.assertEqual("test-email-1", resource.json['member']['email'])

        # When
        member_id = Member.query.get(random.randrange(1, dummy_data_creator.SAMPLE_MEMBER_SIZE[DUMMY_DATA_SIZE] + 1)).id
        payload = json.dumps({
            'email': 'test-email-2'
        })
        resource = self.app.post('members/edit/{}'.format(member_id), data=payload)

        # Then
        self.assertEqual('test-email-2', resource.json['member']['email'])

        # When
        member_id = Member.query.get(random.randrange(1, dummy_data_creator.SAMPLE_MEMBER_SIZE[DUMMY_DATA_SIZE] + 1)).id
        payload = json.dumps({
            'username': 'test-username-3'
        })
        resource = self.app.post('members/edit/{}'.format(member_id), data=payload)

        # Then
        self.assertEqual('test-username-3', resource.json['member']['username'])

        # When
        member_id = Member.query.get(random.randrange(1, dummy_data_creator.SAMPLE_MEMBER_SIZE[DUMMY_DATA_SIZE] + 1)).id
        payload = json.dumps({
            'username': '',
            'email': ''
        })
        resource = self.app.post('members/edit/{}'.format(member_id), data=payload)

        # Then
        self.assertEqual("empty fields", resource.json['err_msg'])

        # When
        member_id = Member.query.get(random.randrange(1, dummy_data_creator.SAMPLE_MEMBER_SIZE[DUMMY_DATA_SIZE] + 1)).id
        payload = json.dumps({

        })
        resource = self.app.post('members/edit/{}'.format(member_id), data=payload)

        # Then
        self.assertEqual("empty fields", resource.json['err_msg'])

        # Where
        payload = json.dumps({  # invalid info type
            'username': 1234,
            'email': 1234
        })
        resource = self.app.post('members/edit/{}'.format(member_id), data=payload)

        # Then
        self.assertEqual("invalid type", resource.json['err_msg'])

    def test_get_all_transactions(self):
        # Where
        transactions = Transaction.query.all()
        resource = self.app.get('transactions/all')

        # Then
        self.assertEqual(len(transactions), len(resource.json['transactions']))
        if len(resource.json['transactions']) > 0:
            self.assertEqual(int, type(resource.json['transactions'][0]['id']))

    def test_issue_book(self):
        # Where

        # creating a new member
        payload = json.dumps({
            'username': 'test-username-1',
            'email': 'test-email-1'
        })
        member_id = self.app.post('members/create', data=payload).json['member']['id']

        # get available book instance
        book_instance_id = BookInstance.query.filter_by(is_available=True).limit(1)[0].id

        payload = json.dumps({
            'book_instance_id': book_instance_id,
            'member_id': member_id,
            'issue_period': random.randrange(200)
        })
        resource = self.app.post('transactions/issue_book', data=payload)

        # Then
        self.assertEqual(int, type(resource.json['transaction']['id']))

        # Where

        payload = json.dumps({

        })
        resource = self.app.post('transactions/issue_book', data=payload)

        # Then
        self.assertEqual('empty fields', resource.json['err_msg'])

        # Where

        payload = json.dumps({
            'book_instance_id': len(BookInstance.query.all()) + 1,
            'member_id': member_id,
            'issue_period': random.randrange(200)
        })
        resource = self.app.post('transactions/issue_book', data=payload)

        # Then
        self.assertEqual('book_instance does not exist', resource.json['err_msg'])

        # Where

        payload = json.dumps({
            'book_instance_id': book_instance_id,
            'member_id': len(Member.query.all()) + 1,
            'issue_period': random.randrange(200)
        })
        resource = self.app.post('transactions/issue_book', data=payload)

        # Then
        self.assertEqual('member does not exist', resource.json['err_msg'])

        # Where

        payload = json.dumps({
            'book_instance_id': book_instance_id,
            'member_id': member_id,
            'issue_period': -10
        })
        resource = self.app.post('transactions/issue_book', data=payload)

        # Then
        self.assertEqual('invalid issue_period', resource.json['err_msg'])

        # Where

        book_instance = BookInstance.query.get(book_instance_id)
        book_instance.is_available = False
        db.session.add(book_instance)
        db.session.commit()

        payload = json.dumps({
            'book_instance_id': book_instance_id,
            'member_id': member_id,
            'issue_period': random.randrange(200)
        })
        resource = self.app.post('transactions/issue_book', data=payload)

        # Then
        self.assertEqual('book unavailable', resource.json['err_msg'])

        # Where

        member = Member.query.get(member_id)
        member.unbilled = 500
        db.session.add(member)

        book_instance = BookInstance.query.get(book_instance_id)
        book_instance.is_available = True
        db.session.add(book_instance)

        db.session.commit()

        payload = json.dumps({
            'book_instance_id': book_instance_id,
            'member_id': member_id,
            'issue_period': random.randrange(200)
        })
        resource = self.app.post('transactions/issue_book', data=payload)

        # Then
        self.assertEqual('max debt reached', resource.json['err_msg'])

    def test_return_book(self):
        # Where

        # creating a new member
        payload = json.dumps({
            'username': 'test-username-1',
            'email': 'test-email-1'
        })
        member_id = self.app.post('members/create', data=payload).json['member']['id']

        # get available book instance
        book_instance_id = BookInstance.query.filter_by(is_available=True).limit(1)[0].id

        # creating a new book issue
        payload = json.dumps({
            'book_instance_id': book_instance_id,
            'member_id': member_id,
            'issue_period': random.randrange(200)
        })
        self.app.post('transactions/issue_book', data=payload)

        # try to return the book just issued
        resource = self.app.get('transactions/return_book/{}'.format(book_instance_id))

        # Then
        self.assertEqual(int, type(resource.json['transaction']['id']))

        # Where

        # try to return the a book which is returned already
        resource = self.app.get('transactions/return_book/{}'.format(book_instance_id))

        # Then
        self.assertEqual('book_instance not issued', resource.json['err_msg'])

    def test_get_all_reports(self):
        # Where

        resource = self.app.get('library/reports/all')

        # Then
        self.assertEqual(list, type(resource.json['reports']))

    def test_get_report(self):
        # Where

        from_date = datetime.today().date() - timedelta(days=100)
        till_date = datetime.today().date()

        payload = json.dumps({
            'from_date': '{}-{}-{}'.format(from_date.year, from_date.month, from_date.day),
            'till_date': '{}-{}-{}'.format(till_date.year, till_date.month, till_date.day)
        })

        resource = self.app.get('library/report', data=payload)

        # Then
        if 'msg' in resource.json:
            self.assertEqual('report not generated', resource.json['msg'])
        else:
            self.assertEqual(int, type(resource.json['report']['books_issued']))

    def tearDown(self):
        dummy_data_creator.clear_data(db.session)


from app.books.models import BookDetail, BookInstance
from app.users.models import Member
from app.transactions.models import Transaction
