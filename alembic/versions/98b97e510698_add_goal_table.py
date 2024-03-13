"""Add goal table

Revision ID: 98b97e510698
Revises: ee74e30fc457
Create Date: 2024-02-25 16:28:20.792896

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98b97e510698'
down_revision: Union[str, None] = 'ee74e30fc457'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('goal',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('target_amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('is_achieved', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_goal_name'), 'goal', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_goal_name'), table_name='goal')
    op.drop_table('goal')
    # ### end Alembic commands ###
