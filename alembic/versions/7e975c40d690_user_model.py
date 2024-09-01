"""User model

Revision ID: a
Revises: 
Create Date: 2024-09-01 09:12:23.178106

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e975c40d690'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('email', sa.String, nullable=False),
                    sa.Column('username', sa.String, unique=True, nullable=False),
                    sa.Column('first_name', sa.String),
                    sa.Column('last_name', sa.String),
                    sa.Column('password', sa.String, nullable=False)
                    )


def downgrade() -> None:
    op.drop_table('users')