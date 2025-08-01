"""or_29556_create_analytics_description_table

Revision ID: 69e162b7847f
Revises: 6cdd3d3f8000
Create Date: 2025-01-09 13:16:46.713423

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "69e162b7847f"
down_revision: Union[str, None] = "6cdd3d3f8000"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                Create table if not exists analytics_and_alert_definitions (
                    analytics_name text primary key,
                    definition text not null,
                    updated_ts timestamp without time zone default current_timestamp
                );
            """,
        ),
    )


def downgrade() -> None:
    pass
