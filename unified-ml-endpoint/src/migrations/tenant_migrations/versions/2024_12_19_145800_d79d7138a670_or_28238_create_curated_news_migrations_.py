"""OR-28238_create_curated_news_migrations_table

Revision ID: d79d7138a670
Revises: 528885c5f8f0
Create Date: 2024-12-17 14:58:00.451311

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "d79d7138a670"
down_revision: Union[str, None] = "528885c5f8f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """CREATE TABLE IF NOT EXISTS CURATED_NEWS_INSIGHTS (
                CREATED_DATE TIMESTAMPTZ,
                CREATED_AT INTEGER,
                CATEGORY_ID VARCHAR(100),
                TITLE VARCHAR(3000),
                CONTENT text,
                TOPIC_NAME VARCHAR(500),
                TOPIC_ID INTEGER,
                RELATED_NEWS JSONB,
                PRIMARY KEY(TITLE, TOPIC_NAME, CREATED_AT))""",
        ),
    )


def downgrade() -> None:
    pass
