"""empty message

Revision ID: a61fa2c15990
Revises:
Create Date: 2022-08-19 17:37:38.755253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a61fa2c15990'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mailings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mail_text', sa.String(), nullable=True),
    sa.Column('user_filter', sa.String(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subscribers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.BigInteger(), nullable=True),
    sa.Column('provider_code', sa.String(), nullable=True),
    sa.Column('tag', sa.String(), nullable=True),
    sa.Column('time_zone', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sent_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('status', sa.Enum('delivered', 'failed', 'pending', name='messagestatus'), nullable=True),
    sa.Column('mailing_id', sa.Integer(), nullable=True),
    sa.Column('subscriber_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['mailing_id'], ['mailings.id'], ),
    sa.ForeignKeyConstraint(['subscriber_id'], ['subscribers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    op.drop_table('subscribers')
    op.drop_table('mailings')
    # ### end Alembic commands ###
