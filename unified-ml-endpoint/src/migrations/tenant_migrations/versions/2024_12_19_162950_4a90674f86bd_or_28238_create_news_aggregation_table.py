"""OR-28238_create_news_aggregation_table

Revision ID: 4a90674f86bd
Revises: d79d7138a670
Create Date: 2024-12-17 16:29:50.651954

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "4a90674f86bd"
down_revision: Union[str, None] = "d79d7138a670"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
create or replace
view news_aggregations as

select
news_id,
source_id,
information_source,
source_rank,
category_id,
description,
title,
publication_date ,
news_type ,
keyword_type as entity_name
from
categories_news_data
where
publication_date > current_date - interval '6 days'
union all

select
news_id,
source_id,
information_source,
source_rank,
category_id,
description,
title,
publication_date ,
news_type,
keyword_type as entity_name
from
keywords_news_data
where
publication_date > current_date - interval '6 days'
union all

select
news_id,
source_id,
information_source,
source_rank,
category_id,
description,
title,
publication_date ,
news_type ,
supplier_name as entity_name
from
suppliers_news_data
where
publication_date > current_date - interval '6 days'
""",
        ),
    )


def downgrade() -> None:
    pass
