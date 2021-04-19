from faker import Faker
import random

from app import db
from app.users import Member, Librarian
from app.books import BookDetail, BookInstance
from app.transactions import Transaction
from datetime import datetime, timedelta

fake = Faker()

# sample size config
SAMPLE_MEMBER_SIZE = {
    'small': 10,
    'mid': 100,
    'large': 500
}
SAMPLE_LIBRARIAN_SIZE = 1
SAMPLE_UNIQUE_BOOK_SIZE = {
    'small': 5,
    'mid': 200,
    'large': 500
}
SAMPLE_BOOK_INSTANCE_SIZE = {
    'small': 50,
    'mid': 1000,
    'large': 2000
}
SAMPLE_TRANSACTION_SIZE = {
    'small': 10,
    'mid': 100,
    'large': 500
}

# print decorator config
ON_COMPLETE_STR = "Done"
STR_SPACING = 40


# TODO: check if unique field elements are unique while setting
def create_dummy_users(size):
    print("creating dummy users")

    print("creating dummy members [{}]".format(SAMPLE_MEMBER_SIZE[size]).ljust(STR_SPACING, '.'), end="")

    # creating member users
    for i in range(0, SAMPLE_MEMBER_SIZE[size]):
        member = Member(
            username=fake.user_name(),
            email=fake.email(),
            password_hash=fake.random_number(8),
            unbilled=0,
            total_paid=0
        )
        db.session.add(member)
        db.session.commit()

    print(ON_COMPLETE_STR)

    print("creating dummy librarian [{}]".format(SAMPLE_LIBRARIAN_SIZE).ljust(STR_SPACING, '.'), end="")

    # creating librarian user
    librarian = Librarian(
        username=fake.user_name(),
        email=fake.company_email(),
        password_hash=fake.random_number(8),
    )
    db.session.add(librarian)
    db.session.commit()

    print(ON_COMPLETE_STR)


def create_dummy_books(size):
    print("creating dummy books")

    print("creating dummy books details [{}]".format(SAMPLE_UNIQUE_BOOK_SIZE[size]).ljust(STR_SPACING, '.'), end="")

    # creating unique book details
    for i in range(0, SAMPLE_UNIQUE_BOOK_SIZE[size]):
        book_detail = BookDetail(
            name=fake.sentence(4),
            description=fake.sentence(10),
            author=fake.name(),
            base_fees=fake.random_int(10, 50),
            popularity=0,  # will be updated once transactions are created
            stock=0  # will be updated once book instances are created
        )
        db.session.add(book_detail)

    print(ON_COMPLETE_STR)

    print("creating dummy books instances [{}]".format(SAMPLE_BOOK_INSTANCE_SIZE[size]).ljust(STR_SPACING, '.'), end="")

    # creating book instance
    for i in range(0, SAMPLE_BOOK_INSTANCE_SIZE[size]):
        book_detail_id = random.randrange(1, SAMPLE_UNIQUE_BOOK_SIZE[size] + 1)
        BookInstance.create_new(book_detail_id)

    print(ON_COMPLETE_STR)


# TODO: make the issue data
def create_dummy_transactions(size):
    print("creating dummy transactions [{}]".format(SAMPLE_TRANSACTION_SIZE[size]).ljust(STR_SPACING, '.'), end="")

    members = Member.query.all()
    book_instances = BookInstance.query.all()

    list_of_issued_books = []
    for i in range(SAMPLE_TRANSACTION_SIZE[size]):
        rnd = random.randrange(2)

        rnd_member = members[random.randrange(SAMPLE_MEMBER_SIZE[size])]

        while True:
            rnd_book_instance = book_instances[random.randrange(SAMPLE_BOOK_INSTANCE_SIZE[size])]
            if rnd_book_instance.id not in list_of_issued_books:
                break

        transaction = Transaction()
        if rnd == 0:  # return the books issued here
            rnd_return_date = datetime.utcnow() - timedelta(days=random.randrange(0, 2000))
            rnd_issue_date = rnd_return_date - timedelta(days=random.randrange(10, 100))

            transaction.issue_book(rnd_book_instance.id, rnd_member.id, random.randrange(10, 60), issue_date=rnd_issue_date)
            transaction.return_book(return_date=rnd_return_date)
        else:  # books issued are not returned yet
            rnd_issue_date = datetime.utcnow() - timedelta(days=random.randrange(0, 75))
            transaction.issue_book(rnd_book_instance.id, rnd_member.id, random.randrange(10, 60), issue_date=rnd_issue_date)
            list_of_issued_books.append(rnd_book_instance.id)

        db.session.add(transaction)
        db.session.commit()

    print(ON_COMPLETE_STR)


def clear_data(session):
    print("cleaning tables")

    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print("deleting {}".format(table.name).ljust(STR_SPACING, '.'), end="")
        session.execute(table.delete())
        print(ON_COMPLETE_STR)
    session.commit()


def add_dummy_data(size):
    print("adding dummy data to the database")

    clear_data(db.session)

    create_dummy_users(size)
    create_dummy_books(size)
    create_dummy_transactions(size)
