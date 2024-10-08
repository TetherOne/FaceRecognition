"""task_image model

Revision ID: ff61d185c5c8
Revises: c1f4ce4defab
Create Date: 2024-09-15 00:35:19.807649

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ff61d185c5c8"
down_revision: Union[str, None] = "c1f4ce4defab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "task_images",
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("task_images")
