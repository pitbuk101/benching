"""OR27246_add_top_ideas_table

Revision ID: c3776665f585
Revises: 44e5382348d1
Create Date: 2024-10-09 23:52:40.316821

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "c3776665f585"
down_revision: Union[str, None] = "44e5382348d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                CREATE TABLE IF NOT EXISTS top_ideas_knowledge_base (
                category_name text,
                analytics_name text,
                opportunity_query_id integer,
                expert_inputs jsonb, -- expert_recommendation, description, application, when_to_apply, where_to_apply_query_id
                PRIMARY KEY (category_name, analytics_name));

                CREATE TABLE IF NOT EXISTS top_ideas_example (
                    idea text PRIMARY KEY,
                    description	text,
                    actions text
                );

                CREATE TABLE IF NOT EXISTS analytics_idea_details (
                    category_name text,
                    analytics_name text,
                    opportunity_query_id integer,
                    opportunity_insight text,
                    impact text,
                    linked_insight jsonb,
                    analytics_ideas jsonb,
                    updated_ts timestamp without time zone default current_timestamp,
                    PRIMARY KEY (category_name, analytics_name)
                );

                CREATE TABLE IF NOT EXISTS top_idea_details (
                    category_name text,
                    file_timestamp text,
                    idea_number integer,
                    idea text,
                    analytics_name text,
                    impact text,
                    linked_insight jsonb,
                    updated_ts timestamp without time zone default current_timestamp,
                    PRIMARY KEY (category_name, file_timestamp, idea_number)
                );

            """,
        ),
    )


def downgrade() -> None:
    pass
