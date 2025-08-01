"""or_29470_add_opportunity_insights_table

Revision ID: 5d57207900a5
Revises: c90ae643ebc7
Create Date: 2025-01-03 12:34:13.364373

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "5d57207900a5"
down_revision: Union[str, None] = "c90ae643ebc7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                CREATE TABLE IF NOT EXISTS extended_opportunity_insights (
                    category_name text,
                    entity_type text,
                    entity_name text,
                    entity_id text,
                    opp_data jsonb
                );

                Alter table extended_opportunity_insights
                Add column if not exists entity_embedding vector(1536);
            """,
        ),
    )


def downgrade() -> None:
    pass
