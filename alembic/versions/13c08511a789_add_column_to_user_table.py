"""add column to user table

Revision ID: 13c08511a789
Revises: 7c1e2e418f25
Create Date: 2024-09-08 06:05:18.401857

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13c08511a789'
down_revision: Union[str, None] = '7c1e2e418f25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('wallet', sa.Numeric(8, 2), default=0, nullable=False))


def downgrade() -> None:
    op.drop_column('users', 'wallet')
