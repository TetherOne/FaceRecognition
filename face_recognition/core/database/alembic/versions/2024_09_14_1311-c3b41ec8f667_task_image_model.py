"""task_image model

Revision ID: c3b41ec8f667
Revises: 37ea2fe142e2
Create Date: 2024-09-14 13:11:57.017451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c3b41ec8f667"
down_revision: Union[str, None] = "37ea2fe142e2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "task_images",
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column(
            "gender", sa.Enum("MALE", "FEMALE", name="genderenum"), nullable=False
        ),
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
