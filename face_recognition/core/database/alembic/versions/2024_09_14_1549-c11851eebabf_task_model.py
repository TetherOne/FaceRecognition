"""task model

Revision ID: c11851eebabf
Revises:
Create Date: 2024-09-14 15:49:21.727311

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c11851eebabf"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("faces", sa.Integer(), nullable=True),
        sa.Column("men", sa.Integer(), nullable=True),
        sa.Column("women", sa.Integer(), nullable=True),
        sa.Column("average_male_age", sa.DECIMAL(precision=10, scale=1), nullable=True),
        sa.Column(
            "average_female_age", sa.DECIMAL(precision=10, scale=1), nullable=True
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("tasks")
