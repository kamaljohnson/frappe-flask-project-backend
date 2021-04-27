"""empty message

Revision ID: 4491d771dfa4
Revises: 
Create Date: 2021-04-27 14:56:36.037415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4491d771dfa4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book_detail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.Column('author', sa.String(length=20), nullable=False),
    sa.Column('img_src', sa.String(length=120), nullable=True),
    sa.Column('base_fees', sa.Integer(), nullable=False),
    sa.Column('popularity', sa.Integer(), nullable=True),
    sa.Column('stock', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_book_detail_popularity'), 'book_detail', ['popularity'], unique=False)
    op.create_table('librarian',
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=200), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('member',
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=200), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('unbilled', sa.Integer(), nullable=True),
    sa.Column('total_paid', sa.Integer(), nullable=True),
    sa.Column('books_taken', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('report',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('books_issued', sa.Integer(), nullable=True),
    sa.Column('books_returned', sa.Integer(), nullable=True),
    sa.Column('earnings', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('book_instance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_available', sa.Boolean(), nullable=True),
    sa.Column('book_detail_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_detail_id'], ['book_detail.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('returned', sa.Boolean(), nullable=True),
    sa.Column('issue_date', sa.Date(), nullable=True),
    sa.Column('due_date', sa.Date(), nullable=True),
    sa.Column('return_date', sa.Date(), nullable=True),
    sa.Column('fees', sa.Integer(), nullable=True),
    sa.Column('member_id', sa.Integer(), nullable=True),
    sa.Column('book_instance_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_instance_id'], ['book_instance.id'], ),
    sa.ForeignKeyConstraint(['member_id'], ['member.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction')
    op.drop_table('book_instance')
    op.drop_table('report')
    op.drop_table('member')
    op.drop_table('librarian')
    op.drop_index(op.f('ix_book_detail_popularity'), table_name='book_detail')
    op.drop_table('book_detail')
    # ### end Alembic commands ###