"""OR26317_add_chat_history_table

Revision ID: d0b1527f50be
Revises: ea11748c5cf5
Create Date: 2024-09-17 14:41:06.710692

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "d0b1527f50be"
down_revision: Union[str, None] = "ea11748c5cf5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS unified_chat_history (
                chat_id text,
                request_id text,
                request_type text,
                request jsonb,
                model_used text,
                response_type text,
                response jsonb,
                created_time timestamp without time zone default current_timestamp,
                PRIMARY KEY (chat_id, request_id, created_time)
            ) partition by range(created_time);

            CREATE INDEX IF NOT EXISTS idx_unified_chat_history_chat_id ON unified_chat_history(chat_id);

            create table IF NOT EXISTS unified_chat_history_sep24
                partition of unified_chat_history
                for values
                from (timestamp '2024-09-01 00:00:00') to (timestamp '2024-10-01 00:00:00');

            create table IF NOT EXISTS unified_chat_history_oct24
                partition of unified_chat_history
                for values
                from (timestamp '2024-10-01 00:00:00') to (timestamp '2024-11-01 00:00:00');

            create table IF NOT EXISTS unified_chat_history_nov24
                partition of unified_chat_history
                for values
                from (timestamp '2024-11-01 00:00:00') to (timestamp '2024-12-01 00:00:00');

            create table IF NOT EXISTS unified_chat_history_dec24
                partition of unified_chat_history
                for values
                from (timestamp '2024-12-01 00:00:00') to (timestamp '2025-01-01 00:00:00');

            """,
        ),
    )


def downgrade() -> None:
    pass
