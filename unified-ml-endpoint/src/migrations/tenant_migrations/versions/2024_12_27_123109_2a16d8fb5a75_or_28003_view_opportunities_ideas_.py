"""or_28003_view_opportunities_ideas_analytics

Revision ID: 2a16d8fb5a75
Revises: 7fe35da0726d
Create Date: 2024-12-24 12:31:09.363397

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "2a16d8fb5a75"
down_revision: Union[str, None] = "cee7443f8022"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                CREATE OR REPLACE VIEW analytics_ideas_opportunities_view AS
                SELECT
                    ti.*,
                    aid.opportunity_insight,
                    tikb.expert_inputs
                FROM (
                    SELECT *
                    FROM top_idea_details
                    WHERE file_timestamp = (
                        SELECT MAX(file_timestamp)
                        FROM top_idea_details
                    )
                ) AS ti
                LEFT JOIN top_ideas_knowledge_base tikb
                    ON ti.analytics_name = tikb.analytics_name
                    AND ti.category_name = tikb.category_name
                LEFT JOIN analytics_idea_details aid
                    ON ti.analytics_name = aid.analytics_name
                    AND ti.category_name = aid.category_name;
            """,
        ),
    )


def downgrade() -> None:
    pass
