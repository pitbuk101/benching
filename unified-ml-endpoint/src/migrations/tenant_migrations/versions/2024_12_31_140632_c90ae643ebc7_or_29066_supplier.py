"""OR-29066_Supplier

Revision ID: c90ae643ebc7
Revises: e27e8b683d20
Create Date: 2024-12-31 14:06:32.383525

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "c90ae643ebc7"
down_revision: Union[str, None] = "e27e8b683d20"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                ALTER TABLE supplier_profile
                ADD COLUMN IF NOT EXISTS country TEXT DEFAULT NULL,
                ADD COLUMN IF NOT EXISTS country_cost_type TEXT DEFAULT NULL;


                DROP VIEW IF EXISTS supplier_profile_with_insights_with_objectives_view_with_saving;

                CREATE MATERIALIZED VIEW supplier_profile_with_insights_with_objectives_view_with_saving as
                select supplier.*,
                json_agg(DISTINCT jsonb_build_object(
                    'insight_id', insight.insight_id,
                    'label', insight.label,
                    'objective', insight.objective,
                    'reinforcements', insight.reinforcements
                )) as insights,
                COALESCE(json_agg(DISTINCT jsonb_build_object(
                    savings.analytics_name, savings.amount))
                    FILTER (WHERE savings.amount IS NOT NULL), '{}') as analytics_name,
                json_agg(DISTINCT jsonb_build_object(
                    'objective', negotiation_objective.objective,
                    'objective_summary', negotiation_objective.objective_summary
                )) as objectives
                from supplier_profile supplier
                left join negotiation_insights insight
                on supplier.supplier_id = insight.supplier_id
                and supplier.category_name = insight.category_name
                left join negotiation_objective negotiation_objective
                on supplier.supplier_id = negotiation_objective.supplier_id
                and supplier.category_name = negotiation_objective.category_name
                left join saving_opportunities savings
                on supplier.supplier_id = savings.supplier_id
                and supplier.category_name = savings.category_name
                group by supplier.supplier_id, supplier.category_name, supplier.period;
            """,
        ),
    )


def downgrade() -> None:
    pass
