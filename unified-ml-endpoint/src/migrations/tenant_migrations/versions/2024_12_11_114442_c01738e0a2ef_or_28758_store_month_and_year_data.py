"""OR-28758_store_month_and_year_data

Revision ID: c01738e0a2ef
Revises: 2570b6137cf0
Create Date: 2024-12-10 11:44:42.839045

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "c01738e0a2ef"
down_revision: Union[str, None] = "2570b6137cf0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                ALTER TABLE insights_master ADD COLUMN created_year_month integer;
                ALTER TABLE idea_generation_context ADD COLUMN created_year_month integer;
            """,
        ),
    )


def downgrade() -> None:
    pass
