"""OR27246_modify_idea_gen_tables

Revision ID: 44e5382348d1
Revises: 172d3d0bcec2
Create Date: 2024-10-09 23:51:51.284998

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "44e5382348d1"
down_revision: Union[str, None] = "172d3d0bcec2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                ALTER TABLE IF EXISTS insights_master
                ADD IF NOT EXISTS updated_at timestamp,
                ADD IF NOT EXISTS rule_id integer;

                ALTER TABLE IF EXISTS idea_generation_context
                ADD IF NOT EXISTS updated_at timestamp,
                ADD IF NOT EXISTS rule_id integer;

            """,
        ),
    )


def downgrade() -> None:
    pass
