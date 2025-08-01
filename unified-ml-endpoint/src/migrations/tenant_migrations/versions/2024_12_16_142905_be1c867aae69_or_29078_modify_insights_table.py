"""or_29078_modify_insights_table

Revision ID: be1c867aae69
Revises: 2570b6137cf0
Create Date: 2024-12-16 14:29:05.434771

"""

# flake8: noqa: E501

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "be1c867aae69"
down_revision: Union[str, None] = "3891c9587286"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                ALTER TABLE negotiation_insights
                ADD COLUMN analytics_name TEXT DEFAULT NULL;

                ALTER TABLE negotiation_objective
                ADD COLUMN analytics_names TEXT[] DEFAULT ARRAY[]::TEXT[];


                CREATE OR REPLACE VIEW supplier_profile_with_insights_with_objectives_view_with_saving as
                select supplier.*,
                       avg(savings.amount) filter (where savings.analytics_name = 'LCC') AS "LCC",
                       avg(savings.amount) filter (where savings.analytics_name = 'Rates Harmonization') AS "rates_harmonization",
                       avg(savings.amount)filter (where  savings.analytics_name = 'Payment Terms Standardization') AS "payment_terms_standardization",
                       avg(savings.amount) filter (where  savings.analytics_name = 'Total Saving opportunity') AS "total_saving_opportunity",
                       avg(savings.amount) filter (where  savings.analytics_name = 'Supplier Consolidation') AS "supplier_consolidation",
                       avg(savings.amount) filter (where  savings.analytics_name = 'OEM non-OEM' ) AS "oem_non_oem",
                       avg(savings.amount) filter (where  savings.analytics_name = 'Parametric Cost Modelling') AS "parametric_cost_modelling",
                       avg(savings.amount) filter (where savings.analytics_name = 'Early Payments') AS "early_payments",
                json_agg(DISTINCT jsonb_build_object(
                    'insight_id', insight.insight_id,
                    'label', insight.label,
                    'objective', insight.objective,
                    'reinforcements', insight.reinforcements,
                    'analytics_name', insight.analytics_name
                )) as insights,
                json_agg(DISTINCT jsonb_build_object(
                    'objective', negotiation_objective.objective,
                    'analytics_names', negotiation_objective.analytics_names,
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
                group by supplier.supplier_id, supplier.category_name;
            """,
        ),
    )


def downgrade() -> None:
    pass
