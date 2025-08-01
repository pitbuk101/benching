"""OR26317_add_ideagen_table

Revision ID: 2b5975397d56
Revises: d0b1527f50be
Create Date: 2024-09-17 14:42:13.872332

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "2b5975397d56"
down_revision: Union[str, None] = "d0b1527f50be"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS category_qna (
                category_name text PRIMARY KEY,
                qna jsonb
            );

            CREATE TABLE IF NOT EXISTS supplier_qna (
                category_name text,
                supplier_name text,
                qna jsonb,
                PRIMARY KEY(category_name, supplier_name)
            );

            CREATE TABLE IF NOT EXISTS sku_qna (
                category_name text,
                sku_id text,
                sku_name text,
                qna jsonb,
                PRIMARY KEY(category_name, sku_id)
            );

            CREATE TABLE IF NOT EXISTS sku_supplier_master (
                    supplier_name text,
                    supplier_id text,
                    spend_last_year DOUBLE PRECISION,
                    spend_ytd DOUBLE PRECISION,
                    sku_id text,
                    sku_name text,
                    spend_across_category_ytd DOUBLE PRECISION,
                    spend_across_category_last_year DOUBLE PRECISION,
                    spend_without_po_ytd DOUBLE PRECISION,
                    spend_without_po_last_year DOUBLE PRECISION,
                    spend_single_source_ytd DOUBLE PRECISION,
                    spend_single_source_last_year DOUBLE PRECISION,
                    supplier_relationship text,
                    negotiation_strategy text,
                    country text,
                    hcc text,
                    category_name text,
                    CONSTRAINT PK_supplier_profile PRIMARY KEY (supplier_id, sku_id, category_name)
            );

            CREATE TABLE IF NOT EXISTS idea_generation_context (
                insight_id int PRIMARY KEY,
                linked_insight jsonb,
                sku_qna text,
                supplier_qna text,
                sku_360 text,
                supplier_360 text,
                category_qna text,
                definitions text,
                recommended_ideas jsonb,
                recommended_rca jsonb,
                category_name text,
                alert_type int NOT NULL,
                alert_name text NOT NULL,
                parameter text,
                impact text,
                label text
            );

            CREATE TABLE IF NOT EXISTS insights_master (
                insight_id int PRIMARY KEY,
                alert_type int NOT NULL,
                alert_name text NOT NULL,
                parameter text,
                label text,
                linked_insight text,
                sku text,
                supplier text,
                created_time text NOT NULL,
                impact text,
                document_id int,
                category_name text,
                objectives text
            );

            """,
        ),
    )


def downgrade() -> None:
    pass
