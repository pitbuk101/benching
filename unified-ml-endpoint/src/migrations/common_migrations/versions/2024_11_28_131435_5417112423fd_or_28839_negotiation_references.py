"""OR-28839_negotiation_references

Revision ID: 5417112423fd
Revises:
Create Date: 2024-11-28 13:14:35.235099

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "5417112423fd"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                CREATE TABLE IF NOT EXISTS negotiation_references (
                l1_objective text,
                l1_objective_description text,
                samples jsonb,
                sample_emails jsonb
                );
            """,
        ),
    )


def downgrade() -> None:
    pass
