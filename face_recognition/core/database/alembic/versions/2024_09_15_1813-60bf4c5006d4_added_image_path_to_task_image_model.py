"""added image path to task image model

Revision ID: 60bf4c5006d4
Revises: d157e04cc726
Create Date: 2024-09-15 18:13:03.414439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "60bf4c5006d4"
down_revision: Union[str, None] = "d157e04cc726"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("task_images", sa.Column("image", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("task_images", "image")
