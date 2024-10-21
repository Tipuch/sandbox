"""empty message

Revision ID: 20a442f17098
Revises: 13e1961b2e28
Create Date: 2024-10-20 12:53:55.015517

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision: str = '20a442f17098'
down_revision: Union[str, None] = '13e1961b2e28'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('passkey',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('challenge', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('timeout', sa.Integer(), nullable=False),
    sa.Column('attestation', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('public_key', sa.LargeBinary(), nullable=False),
    sa.Column('sign_count', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_passkey_user_id'), 'passkey', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_passkey_user_id'), table_name='passkey')
    op.drop_table('passkey')
    # ### end Alembic commands ###
