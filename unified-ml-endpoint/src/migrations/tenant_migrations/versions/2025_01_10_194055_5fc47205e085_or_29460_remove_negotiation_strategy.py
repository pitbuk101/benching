"""OR-29460_remove_negotiation_strategy

Revision ID: 5fc47205e085
Revises: 927075fb934f
Create Date: 2025-01-10 19:40:55.822786

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "5fc47205e085"
down_revision: Union[str, None] = "927075fb934f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                DROP TABLE IF EXISTS negotiation_strategy_details;
            """,
        ),
    )


def downgrade() -> None:
    pass
