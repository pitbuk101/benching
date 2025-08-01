"""OR-28839_email_references

Revision ID: 6db1f49688a1
Revises: 73588fd8ca1e
Create Date: 2024-11-28 16:45:51.143678

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "6db1f49688a1"
down_revision: Union[str, None] = "73588fd8ca1e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
               CREATE TABLE IF NOT EXISTS email_references (
                    archetype text PRIMARY KEY,
                    email_content jsonb
                    );
            """,
        ),
    )


def downgrade() -> None:
    pass
