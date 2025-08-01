"""OR-29415_Changing-data-ingestion-sku-supplier-level

Revision ID: e27e8b683d20
Revises: 9ec2822160e4
Create Date: 2024-12-24 13:55:18.871896

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "e27e8b683d20"
down_revision: Union[str, None] = "9ec2822160e4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                ALTER TABLE sku_supplier_master
                RENAME COLUMN hcc TO country_cost_type;

                ALTER TABLE sku_supplier_master
                ADD COLUMN period int DEFAULT 2023,
                ADD COLUMN contract_count_last_year int DEFAULT 0,
                ADD COLUMN contract_count_ytd int DEFAULT 0,
                ADD COLUMN invoice_count_last_year int DEFAULT 0,
                ADD COLUMN invoice_count_ytd int DEFAULT 0,
                ADD COLUMN multi_source_spend_ytd float DEFAULT 0.0,
                ADD COLUMN payment_term_days int DEFAULT NULL,
                ADD COLUMN payment_terms text DEFAULT NULL,
                ADD COLUMN purchase_order_count_last_year int DEFAULT 0,
                ADD COLUMN purchase_order_count_ytd int DEFAULT 0,
                ADD COLUMN quantity float DEFAULT 0.0,
                ADD COLUMN region text DEFAULT NULL,
                ADD COLUMN reporting_currency varchar(50) DEFAULT 'EUR',
                ADD COLUMN unit_of_measurement text DEFAULT NULL,
                ADD COLUMN unit_price float DEFAULT 0.0,
                ADD COLUMN x_axis_condition_1 text DEFAULT NULL,
                ADD COLUMN x_axis_condition_2 text DEFAULT NULL,
                ADD COLUMN y_axis_condition_1 text DEFAULT NULL,
                DROP COLUMN negotiation_strategy;

                ALTER TABLE sku_supplier_master
                DROP CONSTRAINT PK_supplier_profile;

                ALTER TABLE sku_supplier_master
                ADD CONSTRAINT PK_supplier_profile PRIMARY KEY (supplier_id, sku_id, category_name, period);


                ALTER TABLE supplier_profile
                ADD COLUMN period int DEFAULT 2023,
                ADD COLUMN contract_count_last_year int DEFAULT 0,
                ADD COLUMN contract_count_ytd int DEFAULT 0,
                ADD COLUMN invoice_count_last_year int DEFAULT 0,
                ADD COLUMN invoice_count_ytd int DEFAULT 0,
                ADD COLUMN multi_source_spend_ytd float DEFAULT 0.0,
                ADD COLUMN purchase_order_count_last_year int DEFAULT 0,
                ADD COLUMN purchase_order_count_ytd int DEFAULT 0,
                ADD COLUMN region text DEFAULT NULL,
                ADD COLUMN spend_no_po_last_year float DEFAULT 0,
                ADD COLUMN x_axis_condition_1 text DEFAULT NULL,
                ADD COLUMN x_axis_condition_2 text DEFAULT NULL,
                ADD COLUMN y_axis_condition_1 text DEFAULT NULL,
                ADD COLUMN single_source_spend_last_year float DEFAULT 0;


                ALTER TABLE supplier_profile
                RENAME COLUMN currency_1 TO reporting_currency;

                ALTER TABLE supplier_profile
                DROP CONSTRAINT supplier_profile_pkey CASCADE;

                ALTER TABLE supplier_profile
                ADD CONSTRAINT supplier_profile_pkey PRIMARY KEY (supplier_id, category_name, period);

                ALTER TABLE supplier_qna
                ADD COLUMN period int DEFAULT 2023;

                ALTER TABLE supplier_qna
                DROP CONSTRAINT supplier_qna_pkey CASCADE;

                ALTER TABLE supplier_qna
                ADD CONSTRAINT supplier_qna_pkey PRIMARY KEY (supplier_name, category_name, period);

                ALTER TABLE sku_qna
                ADD COLUMN period int DEFAULT 2023;

                ALTER TABLE sku_qna
                DROP CONSTRAINT sku_qna_pkey CASCADE;

                ALTER TABLE sku_qna
                ADD CONSTRAINT sku_qna_pkey PRIMARY KEY (sku_id, category_name, period);
            """,
        ),
    )


def downgrade() -> None:
    pass
