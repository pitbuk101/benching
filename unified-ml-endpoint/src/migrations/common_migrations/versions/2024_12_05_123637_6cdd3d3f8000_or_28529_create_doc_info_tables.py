"""or_28529_create_doc_info_tables

Revision ID: 6cdd3d3f8000
Revises: 6db1f49688a1
Create Date: 2024-12-05 12:36:37.455695

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "6cdd3d3f8000"
down_revision: Union[str, None] = "6db1f49688a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                CREATE TABLE IF NOT EXISTS document_information (
                        document_name text PRIMARY KEY,
                        document_type text,
                        description text DEFAULT NULL,
                        category_name text,
                        content text,
                        summary text,
                        summary_embedding public.vector(1536),
                        keywords text[] DEFAULT NULL,
                        use_cases text[] DEFAULT NULL,
                        metadata jsonb DEFAULT NULL,
                        updated_ts timestamp without time zone default current_timestamp
                    );

                CREATE TABLE IF NOT EXISTS document_chunks (
                    chunk_id integer,
                    document_name text,
                    chunk_content text,
                    page integer,
                    embedding public.vector(1536),
                    updated_ts timestamp without time zone default current_timestamp,
                    PRIMARY KEY (chunk_id, document_name),
                    CONSTRAINT common_document_chunks_fkey
                    FOREIGN KEY (document_name) REFERENCES document_information(document_name) ON DELETE CASCADE
                );
            """,
        ),
    )


def downgrade() -> None:
    pass
