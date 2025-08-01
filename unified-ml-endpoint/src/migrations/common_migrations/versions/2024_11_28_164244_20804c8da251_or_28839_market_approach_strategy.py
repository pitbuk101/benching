"""OR-28839_market_approach_strategy

Revision ID: 20804c8da251
Revises: 5417112423fd
Create Date: 2024-11-28 16:42:44.863278

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "20804c8da251"
down_revision: Union[str, None] = "5417112423fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                CREATE TABLE IF NOT EXISTS market_approach_strategy(
                    market_approach text PRIMARY KEY,
                    is_auctionable boolean,
                    incumbency integer default 0,
                    category_positioning jsonb,
                    supplier_relationship jsonb
                );
            """,
        ),
    )


def downgrade() -> None:
    pass
