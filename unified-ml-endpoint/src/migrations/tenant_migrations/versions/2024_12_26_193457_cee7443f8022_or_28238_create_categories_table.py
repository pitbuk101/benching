"""OR-28238_create_categories_table

Revision ID: cee7443f8022
Revises: c1bb8873f19c
Create Date: 2024-12-26 19:34:57.408841

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "cee7443f8022"
down_revision: Union[str, None] = "c1bb8873f19c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                create table categories (ID VARCHAR(10), NAME VARCHAR(100))
            """,
        ),
    )


def downgrade() -> None:
    pass
