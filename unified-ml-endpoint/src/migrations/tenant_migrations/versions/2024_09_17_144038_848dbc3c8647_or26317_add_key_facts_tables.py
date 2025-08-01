"""OR26317_add_key_facts_tables

Revision ID: 848dbc3c8647
Revises: 850b3745217d
Create Date: 2024-09-17 14:40:38.149919

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "848dbc3c8647"
down_revision: Union[str, None] = "850b3745217d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
            DROP TABLE IF EXISTS key_facts_configuration;

            CREATE TABLE IF NOT EXISTS key_facts_config (
                category_name text,
                config_name text,
                config jsonb,
                updated_ts timestamp without time zone default current_timestamp,
                PRIMARY KEY (category_name, config_name)
            );

            CREATE TABLE IF NOT EXISTS dax_queries (
                request_id text,
                user_category text,
                user_question text,
                user_question_emb public.vector(1536),
                dax_query_custom_filters text,
                execution_status integer default 0,
                execution_output text,
                summarised_output text,
                positive_feedback boolean,
                updated_ts timestamp without time zone default current_timestamp,
                PRIMARY KEY (request_id, user_category)
            );

            CREATE TABLE IF NOT EXISTS dax_query_examples (
                category_name text,
                user_question text,
                user_question_emb public.vector(1536),
                dax_query text,
                updated_ts timestamp without time zone default current_timestamp,
                PRIMARY KEY (category_name, user_question)
            );

            DROP VIEW IF EXISTS executed_dax_view;

            CREATE OR REPLACE VIEW validated_dax_queries_view as
            select
            dq.user_category as category_name ,
            dq.user_question,
            dq.user_question_emb as user_question_emb,
            dq.dax_query_custom_filters as dax_query
            from dax_queries dq where execution_status =200
            union all
            select
            category_name ,
            user_question ,
            user_question_emb ,
            dax_query
            from dax_query_examples dqe ;

            CREATE TABLE IF NOT EXISTS dashboard_reporting (
            category_name text,
            report_id text,
            report_name text,
            sub_report_name text,
            title text,
            description text,
            PRIMARY KEY (category_name, report_id, sub_report_name)
            );

            """,
        ),
    )


def downgrade() -> None:
    pass
