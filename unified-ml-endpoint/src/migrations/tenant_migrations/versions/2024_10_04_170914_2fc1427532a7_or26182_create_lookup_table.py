"""or26182_create_lookup_table

Revision ID: 2fc1427532a7
Revises: a20d5c5bebbf
Create Date: 2024-10-04 17:09:14.216240

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "2fc1427532a7"
down_revision: Union[str, None] = "a20d5c5bebbf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
               CREATE TABLE IF NOT EXISTS dax_entity_lookup (
                    entity_name text,
                    value_range text,
                    entity_values jsonb,
                    updated_ts timestamp without time zone default current_timestamp,
                    PRIMARY KEY (entity_name, value_range)
                );
            """,
        ),
    )


def downgrade() -> None:
    pass
