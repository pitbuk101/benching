"""or27010_update_source_ai_tables

Revision ID: 50b67947c6cb
Revises: c3776665f585
Create Date: 2024-10-24 12:38:55.666307

"""

# flake8: noqa: E501

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "50b67947c6cb"
down_revision: Union[str, None] = "c3776665f585"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                 DO $$
                DECLARE
                    constraint_name text;
                BEGIN
                    SELECT c.constraint_name INTO constraint_name
                    FROM information_schema.table_constraints c
                    WHERE constraint_schema = current_schema()
                    AND table_name = 'source_ai_data_chunks'
                    AND constraint_type = 'FOREIGN KEY';

                    IF constraint_name IS NOT NULL THEN
                        EXECUTE format('ALTER TABLE source_ai_data_chunks DROP CONSTRAINT %I;', constraint_name);
                    ELSE
                        RAISE NOTICE 'No foreign key constraint found for the table.';
                    END IF;

                    EXECUTE format('ALTER TABLE source_ai_data_chunks ADD CONSTRAINT %I FOREIGN KEY (document_name, category_name, supplier_name, sku_id) REFERENCES source_ai_data_info (document_name, category_name, supplier_name, sku_id) ON DELETE CASCADE;', constraint_name);
                END $$;
            """,
        ),
    )


def downgrade() -> None:
    pass
