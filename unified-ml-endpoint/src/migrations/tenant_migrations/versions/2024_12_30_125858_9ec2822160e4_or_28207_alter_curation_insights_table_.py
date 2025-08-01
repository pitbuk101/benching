"""OR-28207_alter_curation_insights_table_with_id

Revision ID: 9ec2822160e4
Revises: 2a16d8fb5a75
Create Date: 2024-12-30 12:58:58.717498

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "9ec2822160e4"
down_revision: Union[str, None] = "2a16d8fb5a75"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                 alter table curated_news_insights add "id" serial;
            """,
        ),
    )


def downgrade() -> None:
    pass
