"""add cart table

Revision ID: 2fa913e84655
Revises: 13c08511a789
Create Date: 2024-09-08 06:29:55.308394

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2fa913e84655'
down_revision: Union[str, None] = '13c08511a789'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('carts',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
                    sa.Column('banana_id', sa.Integer, sa.ForeignKey('bananas.id', ondelete='CASCADE'), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    )


def downgrade() -> None:
    op.drop_table('carts')
