"""OR-29908_Create_category_name_in_document_view

Revision ID: 932e48014aa3
Revises: 5fc47205e085
Create Date: 2025-01-22 18:39:59.319740

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "932e48014aa3"
down_revision: Union[str, None] = "5fc47205e085"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
            DROP VIEW IF EXISTS combined_document_chunks;

            CREATE OR REPLACE VIEW combined_document_chunks AS
                SELECT
                    t1.document_name AS document_id,
                    t1.chunk_id,
                    t1.chunk_content,
                    t1.page,
                    t1.embedding,
                    dic.category_name
                FROM
                    "common".document_chunks t1
                LEFT JOIN
                    "common".document_information dic
                ON
                    t1.document_name = dic.document_name
                UNION ALL
                SELECT
                    t2.document_id::text,
                    t2.chunk_id,
                    t2.chunk_content,
                    t2.page,
                    t2.embedding,
                    di.category_name
                FROM
                    document_chunks t2
                LEFT JOIN
                    document_information di
                ON
                    t2.document_id = di.document_id;
            """,
        ),
    )


def downgrade() -> None:
    pass
