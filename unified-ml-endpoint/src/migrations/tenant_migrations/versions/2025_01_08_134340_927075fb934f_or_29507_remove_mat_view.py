"""OR-29507_remove_mat_view

Revision ID: 927075fb934f
Revises: 3f2c6961a4e5
Create Date: 2025-01-08 13:43:40.310407

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "927075fb934f"
down_revision: Union[str, None] = "3f2c6961a4e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                DROP MATERIALIZED VIEW IF EXISTS combined_document_chunks;
                DROP MATERIALIZED VIEW IF EXISTS combined_document_information;

                CREATE view combined_document_chunks AS
                SELECT
                    t1.document_name as document_id,
                    t1.chunk_id,
                    t1.chunk_content,
                    t1.page,
                    t1.embedding
                FROM
                    "common".document_chunks t1
                UNION ALL
                SELECT
                    t2.document_id::text,
                    t2.chunk_id,
                    t2.chunk_content,
                    t2.page,
                    t2.embedding
                FROM
                    document_chunks t2;

                CREATE view combined_document_information AS
                SELECT
                    t1.document_name as document_id,
                    t1.document_type,
                    t1.description,
                    t1.category_name,
                    t1.content,
                    t1.summary,
                    t1.summary_embedding,
                    t1.keywords,
                    t1.use_cases,
                    t1.metadata
                FROM
                    "common".document_information t1
                UNION ALL
                SELECT
                    t2.document_id::text,
                    t2.document_type,
                    t2.description,
                    t2.category_name,
                    t2.content,
                    t2.summary,
                    t2.summary_embedding,
                    t2.keywords,
                    t2.use_cases,
                    t2.metadata
                FROM
                    document_information t2;
            """,
        ),
    )


def downgrade() -> None:
    pass
