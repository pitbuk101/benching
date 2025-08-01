"""or28529_create_new_knowledge_base_table

Revision ID: 13a36cf7db30
Revises: 21adf3a9d76b
Create Date: 2024-11-29 11:36:08.856281

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "13a36cf7db30"
down_revision: Union[str, None] = "21adf3a9d76b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                DO $$
                DECLARE
                BEGIN
                    CREATE TABLE IF NOT EXISTS document_information (
                        document_id integer PRIMARY KEY,
                        document_name text,
                        document_type text,
                        description text DEFAULT NULL,
                        category_names text[],
                        content text,
                        summary text,
                        summary_embedding public.vector(1536),
                        keywords text[] DEFAULT NULL,
                        use_cases text[] DEFAULT NULL,
                        metadata jsonb DEFAULT NULL,
                        updated_ts timestamp without time zone default current_timestamp
                    );

                    INSERT INTO document_information (
                    document_id,
                    document_name,
                    document_type,
                    category_names,
                    content,
                    summary,
                    summary_embedding,
                    updated_ts)
                    SELECT
                    di.document_id,
                    di.document_filename as document_name,
                    di.document_type,
                    ARRAY[di.category] as category_names,
                    di.content,
                    di.summary,
                    sc.embedding as summary_embedding,
                    di.updated_ts
                    FROM document_info di LEFT JOIN summary_chunks sc ON di.document_id = sc.document_id
                    ON CONFLICT (document_id) DO NOTHING;

                    CREATE TABLE IF NOT EXISTS contract_details (
                        document_id integer PRIMARY KEY REFERENCES document_information(document_id) ON DELETE CASCADE,
                        region text,
                        supplier text,
                        sku text,
                        entity_extraction jsonb,
                        benchmarking jsonb,
                        clauses jsonb,
                        updated_ts timestamp without time zone default current_timestamp
                    );

                    INSERT INTO contract_details (
                        document_id, region, supplier, sku, entity_extraction, benchmarking, clauses, updated_ts
                    )
                    SELECT
                    document_id, region, supplier, sku, entity_extraction, benchmarking, clauses, updated_ts
                    FROM document_info
                    ON CONFLICT (document_id) DO NOTHING;

                    ALTER TABLE document_chunks ADD CONSTRAINT document_chunks_fkey
                    FOREIGN KEY (document_id) REFERENCES document_information(document_id) ON DELETE CASCADE;

                END $$;
            """,
        ),
    )


def downgrade() -> None:
    pass
