"""OR26317_add_document_ai_tables

Revision ID: 850b3745217d
Revises: 2269533fc7e3
Create Date: 2024-09-17 14:40:21.010683

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "850b3745217d"
down_revision: Union[str, None] = "2269533fc7e3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                CREATE TABLE IF NOT EXISTS document_info (
                document_id integer PRIMARY KEY,
                document_type text,
                region text,
                category text,
                supplier text,
                sku text,
                content text,
                summary text,
                entity_extraction jsonb,
                benchmarking jsonb,
                clauses jsonb,
                document_filename text,
                updated_ts timestamp without time zone default current_timestamp
            );

            CREATE TABLE IF NOT EXISTS document_chunks (
                chunk_id integer,
                document_id integer,
                chunk_content text,
                page integer,
                embedding public.vector(1536),
                updated_ts timestamp without time zone default current_timestamp,
                PRIMARY KEY (chunk_id, document_id)
            );

            CREATE TABLE IF NOT EXISTS summary_chunks (
                chunk_id integer,
                document_id integer,
                chunk_summary text,
                embedding public.vector(1536),
                updated_ts timestamp without time zone default current_timestamp,
                PRIMARY KEY (chunk_id, document_id)
            );

            CREATE TABLE IF NOT EXISTS contract_sku_details (
                document_id integer,
                sku_id text,
                original_code text,
                description text,
                price DOUBLE PRECISION,
                price_type text,
                currency text,
                updated_ts timestamp without time zone default current_timestamp,
                PRIMARY KEY (document_id, description, sku_id, price)
            );

            """,
        ),
    )


def downgrade() -> None:
    pass
