"""OR-29460_carrots_sticks_description

Revision ID: d21528baefc2
Revises: 69e162b7847f
Create Date: 2025-01-10 14:13:46.255883

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "d21528baefc2"
down_revision: Union[str, None] = "69e162b7847f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                CREATE TABLE IF NOT EXISTS carrots_and_sticks (
                    id serial PRIMARY KEY,
                    title text,
                    description text,
                    type varchar(30)
                    );

                CREATE TABLE IF NOT EXISTS negotiation_strategy_details (
                    category_name text PRIMARY KEY,
                    pricing_methodology jsonb,
                    contract_methodology jsonb,
                    is_auctionable boolean,
                    supplier_market_complexity text,
                    business_relevance text,
                    category_positioning text
                );
            """,
        ),
    )


def downgrade() -> None:
    pass
