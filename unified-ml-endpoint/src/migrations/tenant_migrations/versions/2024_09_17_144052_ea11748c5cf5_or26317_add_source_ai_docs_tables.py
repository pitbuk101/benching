"""OR26317_add_source_ai_docs_tables

Revision ID: ea11748c5cf5
Revises: 848dbc3c8647
Create Date: 2024-09-17 14:40:52.867000

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "ea11748c5cf5"
down_revision: Union[str, None] = "848dbc3c8647"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS source_ai_data_info (
                document_name text,
                category_name text,
                supplier_name text,
                sku_id text,
                sku_name text,
                document_type text,
                content text,
                summary text,
                summary_embedding public.vector(1536),
                updated_ts timestamp without time zone default current_timestamp,
                PRIMARY KEY (document_name, category_name, supplier_name, sku_id)
            );

            CREATE TABLE IF NOT EXISTS source_ai_data_chunks (
                document_name text,
                category_name text,
                supplier_name text,
                sku_id text,
                sku_name text,
                chunk_id text,
                chunk_content text,
                chunk_embedding public.vector(1536),
                updated_ts timestamp without time zone default current_timestamp,
                PRIMARY KEY (document_name, category_name, supplier_name, sku_id, chunk_id),
                FOREIGN KEY (document_name, category_name, supplier_name, sku_id) REFERENCES
                source_ai_data_info(document_name, category_name, supplier_name, sku_id)
            );

            """,
        ),
    )


def downgrade() -> None:
    pass
