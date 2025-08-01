"""OR-28238_create_keywords_news_table

Revision ID: 4be2075b9ff4
Revises: fa1905460902
Create Date: 2024-12-11 15:01:22.365216

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "4be2075b9ff4"
down_revision: Union[str, None] = "be1c867aae69"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                CREATE TABLE IF NOT EXISTS KEYWORDS_NEWS_DATA (
                    NEWS_ID VARCHAR(255) PRIMARY KEY,
                    SOURCE_ID VARCHAR(500),
                    INFORMATION_SOURCE VARCHAR(500),
                    SOURCE_RANK VARCHAR(500) ,
                    IMAGE_URL VARCHAR(3000) ,
                    KEYWORD_TYPE_ID VARCHAR(500) ,
                    KEYWORD_NAMES VARCHAR(500) ,
                    CATEGORY_ID VARCHAR(255),
                    CATEGORY_NAME VARCHAR(255) ,
                    KEYWORD_TYPE VARCHAR(500),
                    DESCRIPTION TEXT ,
                    TITLE VARCHAR(3000) ,
                    URL VARCHAR(3000) ,
                    NEWS_TYPE VARCHAR(100),
                    PUBLICATION_DATE TIMESTAMP WITH TIME ZONE)
                    ;
            """,
        ),
    )


def downgrade() -> None:
    pass
