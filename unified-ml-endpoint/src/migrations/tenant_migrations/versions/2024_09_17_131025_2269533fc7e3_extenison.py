"""initial setup

Revision ID: 2269533fc7e3
Revises:
Create Date: 2024-09-17 13:10:25.304359

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "2269533fc7e3"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA public;
            """,
        ),
    )


def downgrade() -> None:
    pass
