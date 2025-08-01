"""create_migration_for_table

Revision ID: c29220d61937
Revises: 932e48014aa3
Create Date: 2025-01-23 12:32:11.200193

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "c29220d61937"
down_revision: Union[str, None] = "932e48014aa3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                create table IF NOT EXISTS unified_chat_history_jan25
                partition of unified_chat_history
                for values
                from (timestamp '2025-01-01 00:00:00') to (timestamp '2025-02-01 00:00:00');

                create table IF NOT EXISTS unified_chat_history_feb25
                partition of unified_chat_history
                for values
                from (timestamp '2025-02-01 00:00:00') to (timestamp '2025-03-01 00:00:00');

                create table IF NOT EXISTS unified_chat_history_mar25
                partition of unified_chat_history
                for values
                from (timestamp '2025-03-01 00:00:00') to (timestamp '2025-04-01 00:00:00');

                create table IF NOT EXISTS unified_chat_history_apr25
                partition of unified_chat_history
                for values
                from (timestamp '2025-04-01 00:00:00') to (timestamp '2025-05-01 00:00:00');

                create table IF NOT EXISTS unified_chat_history_may25
                partition of unified_chat_history
                for values
                from (timestamp '2025-05-01 00:00:00') to (timestamp '2025-06-01 00:00:00');

                create table IF NOT EXISTS unified_chat_history_jun25
                partition of unified_chat_history
                for values
                from (timestamp '2025-06-01 00:00:00') to (timestamp '2025-07-01 00:00:00');
            """,
        ),
    )


def downgrade() -> None:
    pass
