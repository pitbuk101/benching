"""OR26317_add_nf_tables

Revision ID: a20d5c5bebbf
Revises: 2b5975397d56
Create Date: 2024-09-17 14:42:26.878348

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "a20d5c5bebbf"
down_revision: Union[str, None] = "2b5975397d56"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                CREATE TABLE IF NOT EXISTS supplier_profile (
                supplier_id text,
                supplier_name text,
                category_name text,
                number_of_supplier_in_category integer,
                spend_ytd DOUBLE PRECISION,
                spend_last_year DOUBLE PRECISION,
                sku_list jsonb,
                sku_list_name jsonb,
                percentage_spend_across_category_ytd DOUBLE PRECISION,
                percentage_spend_across_category_last_year DOUBLE PRECISION,
                supplier_relationship text,
                supplier_name_embedding vector,
                single_source_spend_ytd DOUBLE PRECISION,
                spend_no_po_ytd DOUBLE PRECISION,
                payment_terms jsonb,
                payment_term_days jsonb,
                payment_term_avg DOUBLE PRECISION,
                currency_1 text,
                PRIMARY KEY (supplier_id, category_name)
                );

                CREATE TABLE IF NOT EXISTS negotiation_relationship_details (
                relationship text PRIMARY KEY,
                expert_input text,
                general_information text,
                argument_strategy text,
                negotiation_strategy text
                );

                CREATE TABLE IF NOT EXISTS negotiation_references (
                l1_objective text,
                l1_objective_description text,
                samples jsonb,
                sample_emails jsonb
                );

                CREATE TABLE IF NOT EXISTS negotiation_insights (
                insight_id int PRIMARY KEY,
                supplier_id text,
                supplier_name text,
                category_name text,
                label text,
                objective text,
                reinforcements jsonb,
                minimum_spend_threshold DOUBLE PRECISION
                );

                CREATE TABLE IF NOT EXISTS negotiation_objective (
                supplier_id text ,
                supplier_name text,
                category_name text,
                objective text,
                objective_summary text,
                CONSTRAINT PK_negotiation_objective PRIMARY KEY (supplier_id, objective, category_name)
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

                CREATE TABLE IF NOT EXISTS market_approach_strategy(
                    market_approach text PRIMARY KEY,
                    is_auctionable boolean,
                    incumbency integer default 0,
                    category_positioning jsonb,
                    supplier_relationship jsonb
                );

                CREATE TABLE IF NOT EXISTS saving_opportunities (
                supplier_id text ,
                supplier_name text,
                category_name text,
                analytics_type text,
                analytics_name text,
                amount DOUBLE PRECISION,
                updated_ts timestamp without time zone default current_timestamp,
                CONSTRAINT PK_saving_opportunities PRIMARY KEY (supplier_id, category_name, analytics_type, analytics_name)
                );

                CREATE TABLE IF NOT EXISTS email_references (
                archetype text PRIMARY KEY,
                email_content jsonb
                );

                CREATE OR REPLACE VIEW qna_view as
                select supplier_name, Null as sku_id, Null as sku_name, category_name, qna from supplier_qna
                union all
                select null as supplier_name, sku_id , sku_name, category_name, qna from sku_qna
                union all
                select null as supplier_name, null as sku_id , null as sku_name, category_name, qna from category_qna;

                CREATE OR REPLACE VIEW supplier_profile_with_insights_with_objectives_view_with_saving as
                select supplier.*,
                    avg(savings.amount) filter (where analytics_name = 'LCC') AS "LCC",
                    avg(savings.amount) filter (where analytics_name = 'Rates Harmonization') AS "rates_harmonization",
                    avg(savings.amount) filter (where analytics_name = 'Payment Terms Standardization')
                    AS "payment_terms_standardization",
                    avg(savings.amount) filter (where analytics_name = 'Total Saving opportunity') AS "total_saving_opportunity",
                    avg(savings.amount) filter (where analytics_name = 'Supplier Consolidation') AS "supplier_consolidation",
                    avg(savings.amount) filter (where analytics_name = 'OEM non-OEM' ) AS "oem_non_oem",
                    avg(savings.amount) filter (where analytics_name = 'Parametric Cost Modelling')
                    AS "parametric_cost_modelling",
                    avg(savings.amount) filter (where analytics_name = 'Early Payments') AS "early_payments",
                json_agg(DISTINCT jsonb_build_object(
                    'insight_id', insight.insight_id,
                    'label', insight.label,
                    'objective', insight.objective,
                    'reinforcements', insight.reinforcements
                )) as insights,
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
                group by supplier.supplier_id, supplier.category_name

            """,
        ),
    )


def downgrade() -> None:
    pass
