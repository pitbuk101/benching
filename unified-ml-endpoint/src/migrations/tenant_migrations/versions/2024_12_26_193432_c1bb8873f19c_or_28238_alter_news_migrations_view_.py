"""OR-28238_alter_news_migrations_view_table

Revision ID: c1bb8873f19c
Revises: fb6dab891e5a
Create Date: 2024-12-26 19:34:32.205230

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "c1bb8873f19c"
down_revision: Union[str, None] = "fb6dab891e5a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                DROP VIEW news_aggregations;

                CREATE OR REPLACE VIEW news_aggregations
AS SELECT categories_news_data.news_id,
    categories_news_data.source_id,
    categories_news_data.information_source,
    categories_news_data.source_rank,
    categories_news_data.category_id,
    categories_news_data.category_name,
    categories_news_data.description,
    categories_news_data.title,
    categories_news_data.publication_date,
    categories_news_data.news_type,
    categories_news_data.category_name AS entity_name
   FROM categories_news_data
  WHERE categories_news_data.publication_date > (CURRENT_DATE - '6 days'::interval)
UNION ALL
 SELECT keywords_news_data.news_id,
    keywords_news_data.source_id,
    keywords_news_data.information_source,
    keywords_news_data.source_rank,
    keywords_news_data.category_id,
    keywords_news_data.category_name,
    keywords_news_data.description,
    keywords_news_data.title,
    keywords_news_data.publication_date,
    keywords_news_data.news_type,
    keywords_news_data.keyword_type AS entity_name
   FROM keywords_news_data
  WHERE keywords_news_data.publication_date > (CURRENT_DATE - '6 days'::interval)
UNION ALL
 SELECT suppliers_news_data.news_id,
    suppliers_news_data.source_id,
    suppliers_news_data.information_source,
    suppliers_news_data.source_rank,
    suppliers_news_data.category_id,
    suppliers_news_data.category_name,
    suppliers_news_data.description,
    suppliers_news_data.title,
    suppliers_news_data.publication_date,
    suppliers_news_data.news_type,
    suppliers_news_data.supplier_name AS entity_name
   FROM suppliers_news_data
  WHERE suppliers_news_data.publication_date > (CURRENT_DATE - '6 days'::interval);
            """,
        ),
    )


def downgrade() -> None:
    pass
