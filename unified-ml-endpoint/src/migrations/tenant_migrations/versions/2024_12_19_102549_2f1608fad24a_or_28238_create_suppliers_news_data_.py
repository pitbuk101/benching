"""OR-28238_create_suppliers_news_data_table

Revision ID: 2f1608fad24a
Revises: f1616b8793d7
Create Date: 2024-12-12 10:25:49.389469

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "2f1608fad24a"
down_revision: Union[str, None] = "f1616b8793d7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
               CREATE TABLE IF NOT EXISTS SUPPLIERS_NEWS_DATA (

                    TOOLS_SUPPLIER_ID VARCHAR(500) ,
                    TOOLS_SUPPLIER_NAME VARCHAR(255) ,
                    SUPPLIER_ID VARCHAR(500) ,
                    PARENT_SUPPLIER_NAME VARCHAR(1000) ,
                    CATEGORY_ID VARCHAR(255) ,
                    CHANNEL VARCHAR(500) ,
                    COUNT VARCHAR(255) ,
                    IMAGE_URL VARCHAR(3000) ,
                    INDUSTRY_NAME VARCHAR(500) ,
                    NEWS_ID VARCHAR(255) PRIMARY KEY ,
                    TITLE VARCHAR(3000) ,
                    LANGUAGE_NAME VARCHAR(255) ,
                    PUBLICATION_DATE TIMESTAMPTZ,
                    SOURCE_ID VARCHAR(255),
                    INFORMATION_SOURCE VARCHAR(500) ,
                    SOURCE_RANK VARCHAR(255),
                    DESCRIPTION TEXT,
                    SUPPLIER_NAME VARCHAR(1000) ,
                    TOPIC_NAME VARCHAR(255),
                    URL VARCHAR(3000),
                    NEWS_TYPE VARCHAR(100),
                    COMPANY_ID VARCHAR(255)
                );
            """,
        ),
    )


def downgrade() -> None:
    pass
