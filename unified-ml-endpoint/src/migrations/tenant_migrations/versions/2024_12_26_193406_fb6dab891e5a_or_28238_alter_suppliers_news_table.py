"""OR-28238_alter_suppliers_news_table

Revision ID: fb6dab891e5a
Revises: ccf4df9c26c1
Create Date: 2024-12-26 19:34:06.065342

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "fb6dab891e5a"
down_revision: Union[str, None] = "ccf4df9c26c1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                 alter table suppliers_news_data add category_name varchar(200)
            """,
        ),
    )


def downgrade() -> None:
    pass
