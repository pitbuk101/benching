"""or28099_create_opportunity_insights_table

Revision ID: 21adf3a9d76b
Revises: 50b67947c6cb
Create Date: 2024-10-30 01:14:20.808008

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "21adf3a9d76b"
down_revision: Union[str, None] = "50b67947c6cb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                CREATE TABLE IF NOT EXISTS opportunity_insights (
                    category_name text,
                    insight_id integer,
                    analytics_name text,
                    opportunity_insight text,
                    impact text,
                    linked_insight jsonb,
                    updated_ts timestamp without time zone default current_timestamp,
                    PRIMARY KEY (category_name, insight_id)
                );
            """,
        ),
    )


def downgrade() -> None:
    pass
