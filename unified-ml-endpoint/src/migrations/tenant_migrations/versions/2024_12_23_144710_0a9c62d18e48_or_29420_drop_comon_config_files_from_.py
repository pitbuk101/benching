"""OR-29420_drop_comon_config_files_from_tenant_schema

Revision ID: 0a9c62d18e48
Revises: 7fe35da0726d
Create Date: 2024-12-23 14:47:10.402159

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "0a9c62d18e48"
down_revision: Union[str, None] = "7fe35da0726d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                DROP TABLE IF EXISTS negotiation_references;
                DROP TABLE IF EXISTS market_approach_strategy;
                DROP TABLE IF EXISTS negotiation_relationship_details;
                DROP TABLE IF EXISTS email_references;
            """,
        ),
    )


def downgrade() -> None:
    pass
