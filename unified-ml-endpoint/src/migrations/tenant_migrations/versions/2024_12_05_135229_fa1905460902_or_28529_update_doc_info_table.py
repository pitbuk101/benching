"""or_28529_update_doc_info_table

Revision ID: fa1905460902
Revises: 13a36cf7db30
Create Date: 2024-12-05 13:52:29.182008

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "fa1905460902"
down_revision: Union[str, None] = "13a36cf7db30"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                ALTER TABLE document_information
                ADD column category_name text;

                ALTER TABLE document_information
                ALTER column category_names set default '{}'::text[];

                UPDATE document_information
                set category_name =
                case
                    when array_length(category_names, 1) > 0 then category_names[1]
                    else ''
                end;
            """,
        ),
    )


def downgrade() -> None:
    pass
