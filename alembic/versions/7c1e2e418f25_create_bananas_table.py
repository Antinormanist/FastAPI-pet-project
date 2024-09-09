"""create bananas table

Revision ID: 7c1e2e418f25
Revises: 62d7deb09906
Create Date: 2024-09-04 17:35:39.141917

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c1e2e418f25'
down_revision: Union[str, None] = '62d7deb09906'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('bananas',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('name', sa.String, nullable=False),
                    sa.Column('description', sa.Text),
                    sa.Column('image', sa.LargeBinary, nullable=False),
                    sa.Column('price', sa.Numeric(precision=8, scale=2), nullable=False),
                    sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    )


def downgrade() -> None:
    op.drop_table('bananas')
