"""OR-28758_seed_the_created_month_year_table_with_data

Revision ID: 3891c9587286
Revises: c01738e0a2ef
Create Date: 2024-12-10 13:43:31.481656

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "3891c9587286"
down_revision: Union[str, None] = "c01738e0a2ef"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                UPDATE insights_master set created_year_month = (to_char(CURRENT_TIMESTAMP, 'YYYYMM'::text))::integer;
                UPDATE idea_generation_context set created_year_month = (to_char(CURRENT_TIMESTAMP, 'YYYYMM'::text))::integer;
            """,
        ),
    )


def downgrade() -> None:
    pass
