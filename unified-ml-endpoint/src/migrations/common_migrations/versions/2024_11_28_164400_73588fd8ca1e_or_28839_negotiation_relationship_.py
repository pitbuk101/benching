"""OR-28839_negotiation_relationship_details

Revision ID: 73588fd8ca1e
Revises: 20804c8da251
Create Date: 2024-11-28 16:44:00.164755

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "73588fd8ca1e"
down_revision: Union[str, None] = "20804c8da251"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS negotiation_relationship_details (
                relationship text PRIMARY KEY,
                expert_input text,
                general_information text,
                argument_strategy text,
                negotiation_strategy text
                );
            """,
        ),
    )


def downgrade() -> None:
    pass
