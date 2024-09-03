"""add timestamps

Revision ID: 0d073bd918a3
Revises: 2e08e2e6eed8
Create Date: 2024-09-03 14:48:43.113337

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0d073bd918a3"
down_revision: Union[str, None] = "2e08e2e6eed8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("comment", sa.Column("created_at", sa.DateTime(), nullable=False))
    op.add_column("comment", sa.Column("updated_at", sa.DateTime(), nullable=False))
    op.add_column("post", sa.Column("created_at", sa.DateTime(), nullable=False))
    op.add_column("post", sa.Column("updated_at", sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("post", "updated_at")
    op.drop_column("post", "created_at")
    op.drop_column("comment", "updated_at")
    op.drop_column("comment", "created_at")
    # ### end Alembic commands ###
