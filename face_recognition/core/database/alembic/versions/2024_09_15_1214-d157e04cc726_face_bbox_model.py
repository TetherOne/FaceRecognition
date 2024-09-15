"""face_bbox model

Revision ID: d157e04cc726
Revises: a62043c24f45
Create Date: 2024-09-15 12:14:48.790845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d157e04cc726"
down_revision: Union[str, None] = "a62043c24f45"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "bounding_box_faces",
        sa.Column("height", sa.Integer(), nullable=False),
        sa.Column("width", sa.Integer(), nullable=False),
        sa.Column("x", sa.Integer(), nullable=False),
        sa.Column("y", sa.Integer(), nullable=False),
        sa.Column("face_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.CheckConstraint("height >= 0 and height <= 1079"),
        sa.CheckConstraint("width >= 0 and width <= 1919"),
        sa.CheckConstraint("x >= 0 and x <= 1919"),
        sa.CheckConstraint("y >= 0 and y <= 1079"),
        sa.ForeignKeyConstraint(
            ["face_id"],
            ["image_faces.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("face_id"),
    )


def downgrade() -> None:
    op.drop_table("bounding_box_faces")
