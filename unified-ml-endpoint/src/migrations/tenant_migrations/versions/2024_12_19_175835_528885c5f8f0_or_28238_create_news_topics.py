"""OR-28238_create_news_topics

Revision ID: 528885c5f8f0
Revises: 2f1608fad24a
Create Date: 2024-12-16 17:58:35.761971

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "528885c5f8f0"
down_revision: Union[str, None] = "2f1608fad24a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                CREATE TABLE IF NOT EXISTS NEWS_TOPICS (
                    ID integer PRIMARY KEY ,
                    NAME VARCHAR(500)
                );
            """,
        ),
    )


def downgrade() -> None:
    pass
