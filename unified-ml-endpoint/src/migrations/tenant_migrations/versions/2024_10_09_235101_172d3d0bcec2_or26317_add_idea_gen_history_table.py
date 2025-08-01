"""OR26317_add_idea_gen_history_table

Revision ID: 172d3d0bcec2
Revises: 2fc1427532a7
Create Date: 2024-10-09 23:51:01.478591

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "172d3d0bcec2"
down_revision: Union[str, None] = "2fc1427532a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                CREATE TABLE IF NOT EXISTS chat_history (
                chat_id text PRIMARY KEY,
                recommended_rca jsonb,
                recommended_ideas jsonb,
                chat_message_history jsonb
            );

            """,
        ),
    )


def downgrade() -> None:
    pass
