"""create users table

Revision ID: 62d7deb09906
Revises: 
Create Date: 2024-09-04 17:30:26.588565

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62d7deb09906'
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
