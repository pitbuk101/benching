"""OR-28242_alter_news_curations_table

Revision ID: ccf4df9c26c1
Revises: 0a9c62d18e48
Create Date: 2024-12-26 19:33:21.673373

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "ccf4df9c26c1"
down_revision: Union[str, None] = "0a9c62d18e48"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
               alter table curated_news_insights add category_name varchar(200);
            """,
        ),
    )


def downgrade() -> None:
    pass
