"""OR-28238_create_news_feed_status_table

Revision ID: 7fe35da0726d
Revises: 4a90674f86bd
Create Date: 2024-12-18 18:23:54.751215

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "7fe35da0726d"
down_revision: Union[str, None] = "4a90674f86bd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                create table NEWS_FEED_STATUS (STATUS VARCHAR(30),DATE_RUN TIMESTAMPTZ, DATE_RUN_INT INTEGER);
            """,
        ),
    )


def downgrade() -> None:
    pass
