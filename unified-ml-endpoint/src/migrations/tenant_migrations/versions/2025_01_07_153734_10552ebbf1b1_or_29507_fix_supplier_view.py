"""OR-29507_Fix_supplier_view

Revision ID: 10552ebbf1b1
Revises: 70af3f6e1080
Create Date: 2025-01-07 15:37:34.169401

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "10552ebbf1b1"
down_revision: Union[str, None] = "70af3f6e1080"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                DROP MATERIALIZED VIEW IF EXISTS supplier_profile_with_insights_with_objectives_view_with_saving CASCADE;

                CREATE MATERIALIZED VIEW supplier_profile_with_insights_with_objectives_view_with_saving as
                select supplier.*,
                json_agg(DISTINCT jsonb_build_object(
                    'insight_id', insight.insight_id,
                    'label', insight.label,
                    'objective', insight.objective,
                    'reinforcements', insight.reinforcements,
                    'analytics_name', insight.analytics_name
                )) as insights,
                COALESCE(json_agg(DISTINCT jsonb_build_object(
                    savings.analytics_name, savings.amount))
                    FILTER (WHERE savings.amount IS NOT NULL), '{}') as analytics_name,
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
                group by supplier.supplier_id, supplier.category_name, supplier.period;

                CREATE OR REPLACE VIEW extended_supplier_profile
                as select * from  supplier_profile_with_insights_with_objectives_view_with_saving
                union all
                select
                    entity_id as supplier_id,
                    entity_name as supplier_name,
                    category_name,
                    NULl as number_of_supplier_in_category,
                    NULl as spend_ytd,
                    NULl as spend_last_year,
                    NULl as sku_list,
                    NULl as sku_list_name,
                    NULl as percentage_spend_across_category_ytd,
                    NULl as percentage_spend_across_category_last_year,
                    NULl as supplier_relationship,
                    entity_embedding as supplier_name_embedding,
                    NULl as single_source_spend_ytd,
                    NULl as spend_no_po_ytd,
                    NULl as payment_terms,
                    NULl as payment_term_days,
                    NULl as payment_term_avg,
                    NULl as reporting_currency,
                    NULl as country,
                    NULl as country_cost_type,
                    NULl as period,
                    NULl as contract_count_last_year,
                    NULl as contract_count_ytd,
                    NULl as invoice_count_last_year,
                    NULl as invoice_count_ytd,
                    NULl as multi_source_spend_ytd,
                    NULl as purchase_order_count_last_year,
                    NULl as purchase_order_count_ytd,
                    NULl as region,
                    NULl as spend_no_po_last_year,
                    NULl as x_axis_condition_1,
                    NULl as x_axis_condition_2,
                    NULl as y_axis_condition_1,
                    NULl as single_source_spend_last_year,
                    NULl as insights,
                    opp_data::json as analytics_name,
                    NULl as objectives
                from extended_opportunity_insights where entity_type = 'Supplier';

            """,
        ),
    )


def downgrade() -> None:
    pass
