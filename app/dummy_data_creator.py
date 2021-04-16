from faker import Faker
import random

from app import db
from app.users import Member, Librarian
from app.books import BookDetail, BookInstance
from app.transactions import Transaction

fake = Faker()

# sample size config
SAMPLE_MEMBER_SIZE = 100
SAMPLE_LIBRARIAN_SIZE = 1
SAMPLE_UNIQUE_BOOK_SIZE = 500
SAMPLE_BOOK_INSTANCE_SIZE = 2000
SAMPLE_TRANSACTION_SIZE = 500

# print decorator config
ON_COMPLETE_STR = "Done"
STR_SPACING = 40


# TODO: check if unique field elements are unique while setting
def create_dummy_users():
    print("creating dummy users")

    print("creating dummy members [{}]".format(SAMPLE_MEMBER_SIZE).ljust(STR_SPACING, '.'), end="")

    # creating member users
    for i in range(0, SAMPLE_MEMBER_SIZE):
        member = Member(
            username=fake.user_name(),
            email=fake.email(),
            password_hash=fake.random_number(8),
            unbilled=fake.random_int(0, 500),
            total_paid=fake.random_int(0, 5000)
        )
        db.session.add(member)
        db.session.commit()

    print(ON_COMPLETE_STR)

    print("creating dummy members [{}]".format(SAMPLE_LIBRARIAN_SIZE).ljust(STR_SPACING, '.'), end="")

    # creating librarian user
    librarian = Librarian(
        username=fake.user_name(),
        email=fake.company_email(),
        password_hash=fake.random_number(8),
    )
    db.session.add(librarian)
    db.session.commit()

    print(ON_COMPLETE_STR)


def create_dummy_books():
    print("creating dummy books")

    print("creating dummy books details [{}]".format(SAMPLE_UNIQUE_BOOK_SIZE).ljust(STR_SPACING, '.'), end="")

    # creating unique book details
    for i in range(0, SAMPLE_UNIQUE_BOOK_SIZE):
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

    print("creating dummy books instances [{}]".format(SAMPLE_BOOK_INSTANCE_SIZE).ljust(STR_SPACING, '.'), end="")

    # creating book instance
    for i in range(0, SAMPLE_BOOK_INSTANCE_SIZE):
        book_instances = BookInstance(
            is_available=True,  # will be updated when transactions are created
            book_detail_id=random.randrange(1, SAMPLE_UNIQUE_BOOK_SIZE + 1)
        )
        db.session.add(book_instances)

    db.session.commit()

    print(ON_COMPLETE_STR)


# TODO create dummy transactions
def create_dummy_transactions():
    print("creating dummy transactions [{}]".format(SAMPLE_TRANSACTION_SIZE).ljust(STR_SPACING, '.'), end="")
    print(ON_COMPLETE_STR)


def clear_data(session):
    print("cleaning tables")

    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print("deleting {}".format(table.name).ljust(STR_SPACING, '.'), end="")
        session.execute(table.delete())
        print(ON_COMPLETE_STR)
    session.commit()


def add_dummy_data():
    print("adding dummy data to the database")

    clear_data(db.session)

    create_dummy_users()
    create_dummy_books()
    create_dummy_transactions()
