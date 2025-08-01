import pandas as pd
from datetime import datetime
from ada.components.db.sf_connector import SnowflakeClient
from ada.use_cases.quick_nego.model import CurrencySymbol
import json
def get_supplier_data(  # pylint: disable=too-many-branches
    sf_client: SnowflakeClient,
    script_type: str,
    value=10,
    category: str="Bearings",
) -> tuple[pd.DataFrame, str]:
    order = "desc" if script_type == "top_supplier" else "asc"
    supplier_data = pd.DataFrame(
        sf_client.select_records_with_filter(
            table_name='Data.NEGO_SUPPLIER_MASTER',
            filtered_columns=[
                "SUPPLIER as supplier_name",
                "YEAR",
                "SUM(spend_ytd) as spend",
                "MAX(CURRENCY_SYMBOL) AS CURRENCY_SYMBOL",
                "(ROUND(SUM(PERCENTAGE_SPEND_ACROSS_CATEGORY_YTD),2)) AS PERCENTAGE_SPEND_CONTRIBUTION",
            ],
            filter_condition=(
                f"LOWER(category) = LOWER('{category}') AND NUMBER_OF_SKU>=1 AND YEAR = (SELECT MAX(YEAR) FROM Data.NEGO_SUPPLIER_MASTER )"
            ),
            group_by=["supplier_name", "YEAR"],
            order_by=("sum(spend_ytd)", order),
            num_records=value,
        )
    )
    supplier_data.columns = supplier_data.columns.str.lower()
    supplier_data["currency_symbol"].fillna(" ", inplace=True)
    supplier_data["percentage_spend_contribution"] = supplier_data["percentage_spend_contribution"].astype(float)
    valid_suppliers_df = sf_client.fetch_dataframe("""
        SELECT DISTINCT SUPPLIER_NAME AS supplier_name
        FROM Data.T_C_NEGOTIATION_FACTORY_T2
        WHERE SKU_ID != '-1'
    """)
    valid_suppliers_df.columns = valid_suppliers_df.columns.str.lower()

    if not valid_suppliers_df.empty:
        supplier_data = supplier_data[supplier_data["supplier_name"].isin(valid_suppliers_df["supplier_name"])]
    else:
        supplier_data = pd.DataFrame()

    return supplier_data, category

def render_structured_insights_from_db(db_results):
    """
    Converts raw JSON strings into structured dictionary format for rendering insights.

    Args:
        spend_json (str): JSON string from spend insight response.
        supplier_json (str): JSON string from supplier insight response.
        opportunity_json (str): JSON string from opportunity insight response.
        market_insights (list, optional): List of market-level insights.
        others (list, optional): List of miscellaneous insights.

    Returns:
        dict: Structured dictionary containing organized insights.
    """
    spend_insights = []
    supplier_insights = []
    market_insights = []
    opportunity_data = {}
    others = []

    for _, row in db_results.iterrows():
        analytics_type = row['ANALYTICS']
        try:
            response = json.loads(row['RESPONSE']) if isinstance(row['RESPONSE'], str) else row['RESPONSE']

            if analytics_type == "Spend":
                spend_insights.extend(response if isinstance(response, list) else [response])
            elif analytics_type == "Supplier":
                supplier_insights.extend(response if isinstance(response, list) else [response])
            elif analytics_type == "Market":
                market_insights.extend(response if isinstance(response, list) else [response])
            elif analytics_type == "Opportunity":
                for key, value in response.items():
                    if key not in opportunity_data:
                        opportunity_data[key] = {
                            "opportunity": value.get("opportunity", 0),
                            "insights": value.get("insights", []) if value.get("opportunity", 0) > 0 else []
                        }
                    else:
                        # Combine opportunity values
                        opportunity_data[key]["opportunity"] += value.get("opportunity", 0)
                        opportunity_data[key]["insights"].extend(
                            value.get("insights", []) if value.get("opportunity", 0) > 0 else []
                        )
            else:
                others.append(row)

        except json.JSONDecodeError as e:
            print(f"Invalid JSON format in analytics '{analytics_type}': {e}")
            return {"error": f"Invalid JSON in {analytics_type}"}

    return {
        "Spend": spend_insights if spend_insights else [],
        "Market": market_insights if market_insights else [],
        "Suppliers": supplier_insights if supplier_insights else [],
        "Opportunity": opportunity_data if opportunity_data else {},
        "Others": others or []
    }

def get_supplier_insight(
    sf_client: SnowflakeClient,
    supplier_name: str,
    category: str,
    skus: list = None,
) -> list:
   # skus is a list
    materials_formatted = ", ".join(f"'{m}'" for m in skus)
    print("Materials Formatted: ", materials_formatted)

    query = f"""
    SELECT * FROM DATA.NEGOTIATION_INSIGHTS_MASTER
    WHERE
        (SUPPLIER = '{supplier_name}' AND MATERIAL IN ({materials_formatted})) OR 
        (SUPPLIER = '{supplier_name}' AND MATERIAL = 'NULL')
        AND CATEGORY = '{category}'
    """
    supplier_data = sf_client.fetch_dataframe(query)
    insight = render_structured_insights_from_db(supplier_data)
    print("Supplier Insights:-------", insight)
    #supplier_data = sf_client.fetch_dataframe(f"SELECT RESPONSE FROM data.negotiation_insights_master WHERE SUPPLIER='{supplier_name}' AND category='{category}' AND response !='[]'")
    #insight = supplier_data["RESPONSE"].apply(lambda x: x.strip('[]').replace('"', '')).tolist()
    return insight

def get_all_suppliers(
        sf_client: SnowflakeClient,
        category: str,
) -> list:
    """Fetch all suppliers for a given category."""
    query = f"""SELECT 
            SUPPLIER AS supplier_name,
            YEAR,
            SUM(spend_ytd) AS spend,
            MAX(CURRENCY_SYMBOL) AS CURRENCY_SYMBOL,
            ROUND(SUM(PERCENTAGE_SPEND_ACROSS_CATEGORY_YTD), 2) AS PERCENTAGE_SPEND_CONTRIBUTION
        FROM 
            DATA.NEGO_SUPPLIER_MASTER
        WHERE 
            LOWER(category) = LOWER('{category}')
            AND NUMBER_OF_SKU >= 1
            AND YEAR = (SELECT MAX(YEAR) FROM DATA.NEGO_SUPPLIER_MASTER)
        GROUP BY 
            SUPPLIER, YEAR
        ORDER BY 
            spend DESC;"""
   #query = f"SELECT DISTINCT SUPPLIER_NAME from data.T_C_NEGOTIATION_FACTORY_T2 where period='2025' and category_name='{category}' and multi_source_spend_ytd>0"
    supplier_data = sf_client.fetch_dataframe(query)
    supplier_data.columns = supplier_data.columns.str.lower()
    suppliers = supplier_data.to_json(orient='records', date_format='iso')
    return suppliers
def get_supplier_having_alternatives(
    sf_client: SnowflakeClient,
    category: str ,
) -> list:
    """Fetch suppliers having alternatives for a given supplier and category."""
    query = f"""
        Select distinct primary_supplier as SUPPLIER_NAME from (WITH supplier_count_data AS (
            SELECT
                PERIOD AS YEAR,
                CATEGORY_NAME AS CATEGORY,
                SKU_NAME as sku,
                COUNT(DISTINCT SUPPLIER_NAME) AS supplier_count
            FROM data.T_C_NEGOTIATION_FACTORY_T2
            where PERIOD='2025' and category='{category}'
            GROUP BY PERIOD, CATEGORY_NAME, SKU_NAME
        ),
        primary_supplier_data AS (
            SELECT
                PERIOD AS YEAR,
                CATEGORY_NAME AS CATEGORY,
                SUPPLIER_NAME AS primary_supplier,
                SKU_NAME as sku,
                AVG(UNIT_PRICE) AS avg_unit_price,
                SUM(QUANTITY) AS total_quantity,
                ROW_NUMBER() OVER (
                    PARTITION BY PERIOD, CATEGORY_NAME, SKU_NAME 
                    ORDER BY SUM(QUANTITY) DESC, AVG(UNIT_PRICE) ASC
                ) as primary_rank
            FROM data.T_C_NEGOTIATION_FACTORY_T2
            where PERIOD='2025' and CATEGORY_NAME='{category}'
            GROUP BY PERIOD, CATEGORY_NAME, SUPPLIER_NAME, SKU_NAME
        ),
        filtered_primary_data AS (
            SELECT * FROM primary_supplier_data WHERE primary_rank = 1
        ),
        alternate_suppliers AS (
            SELECT
                sc.PERIOD AS YEAR,
                sc.CATEGORY_NAME AS CATEGORY,
                sc.SKU_NAME as sku,
                sc.SUPPLIER_NAME AS alternate_supplier,
                AVG(sc.UNIT_PRICE) AS alternate_price,
                ROW_NUMBER() OVER (
                    PARTITION BY sc.PERIOD, sc.CATEGORY_NAME, sc.SKU_NAME
                    ORDER BY AVG(sc.UNIT_PRICE) ASC
                ) as price_rank
            FROM data.T_C_NEGOTIATION_FACTORY_T2 sc
            JOIN filtered_primary_data psd ON sc.SKU_NAME = psd.sku 
                AND sc.PERIOD = psd.YEAR 
                AND sc.CATEGORY_NAME = psd.CATEGORY
            WHERE sc.SUPPLIER_NAME != psd.primary_supplier
            GROUP BY sc.PERIOD, sc.CATEGORY_NAME, sc.SKU_NAME, sc.SUPPLIER_NAME
        )
        SELECT
            psd.YEAR,
            psd.CATEGORY,
            psd.primary_supplier,
            psd.sku,
            psd.total_quantity,
            psd.avg_unit_price,
            -- Multisourcing information
            scd.supplier_count,
            CASE 
                WHEN scd.supplier_count > 1 THEN 'MULTISOURCED'
                ELSE 'SINGLE_SOURCE'
            END AS sourcing_status,
            -- Alternate supplier information
            alt1.alternate_supplier AS best_alternate_supplier,
            alt1.alternate_price AS best_alternate_price,
            ROUND((psd.avg_unit_price - alt1.alternate_price) / psd.avg_unit_price * 100, 2) AS potential_savings_pct,
            alt2.alternate_supplier AS second_alternate_supplier,
            alt2.alternate_price AS second_alternate_price,
            -- Price comparison metrics
            CASE
                WHEN alt1.alternate_price < psd.avg_unit_price THEN 'BETTER_PRICE_AVAILABLE'
                WHEN alt1.alternate_price = psd.avg_unit_price THEN 'COMPETITIVE_PRICE'
                ELSE 'CURRENT_BEST_PRICE'
            END AS price_status
        FROM filtered_primary_data psd
        LEFT JOIN supplier_count_data scd ON psd.YEAR = scd.YEAR 
            AND psd.CATEGORY = scd.CATEGORY 
            AND psd.sku = scd.sku
        LEFT JOIN alternate_suppliers alt1 ON psd.YEAR = alt1.YEAR 
            AND psd.CATEGORY = alt1.CATEGORY 
            AND psd.sku = alt1.sku 
            AND alt1.price_rank = 1 
        LEFT JOIN alternate_suppliers alt2 ON psd.YEAR = alt2.YEAR 
            AND psd.CATEGORY = alt2.CATEGORY 
            AND psd.sku = alt2.sku 
            AND alt2.price_rank = 2
        where  scd.supplier_count>1)
    """
    suppliers = sf_client.fetch_dataframe(query)
    suppliers_list = suppliers["SUPPLIER_NAME"].tolist()
  
    return suppliers_list


def get_batna_details(
    sf_client: SnowflakeClient,
    supplier_name: str,
    category: str,
) -> list:
    """Fetch alternative suppliers for a given supplier and category."""
    query = f"""
        WITH supplier_count_data AS (
            SELECT
                PERIOD AS YEAR,
                CATEGORY_NAME AS CATEGORY,
                SKU_NAME as sku,
                COUNT(DISTINCT SUPPLIER_NAME) AS supplier_count
            FROM Data.T_C_NEGOTIATION_FACTORY_T2
            where PERIOD='2025' and category='{category}'
            GROUP BY PERIOD, CATEGORY_NAME, SKU_NAME
        ),
        primary_supplier_data AS (
            SELECT
                PERIOD AS YEAR,
                CATEGORY_NAME AS CATEGORY,
                SUPPLIER_NAME AS primary_supplier,
                SKU_NAME as sku,
                AVG(UNIT_PRICE) AS avg_unit_price,
                SUM(QUANTITY) AS total_quantity,
                ROW_NUMBER() OVER (
                    PARTITION BY PERIOD, CATEGORY_NAME, SKU_NAME 
                    ORDER BY SUM(QUANTITY) DESC, AVG(UNIT_PRICE) ASC
                ) as primary_rank
            FROM Data.T_C_NEGOTIATION_FACTORY_T2
            where PERIOD='2025' and CATEGORY_NAME='{category}'
            GROUP BY PERIOD, CATEGORY_NAME, SUPPLIER_NAME, SKU_NAME
        ),
        filtered_primary_data AS (
            SELECT * FROM primary_supplier_data WHERE primary_rank = 1
        ),
        alternate_suppliers AS (
            SELECT
                sc.PERIOD AS YEAR,
                sc.CATEGORY_NAME AS CATEGORY,
                sc.SKU_NAME as sku,
                sc.SUPPLIER_NAME AS alternate_supplier,
                AVG(sc.UNIT_PRICE) AS alternate_price,
                ROW_NUMBER() OVER (
                    PARTITION BY sc.PERIOD, sc.CATEGORY_NAME, sc.SKU_NAME
                    ORDER BY AVG(sc.UNIT_PRICE) ASC
                ) as price_rank
            FROM Data.T_C_NEGOTIATION_FACTORY_T2 sc
            JOIN filtered_primary_data psd ON sc.SKU_NAME = psd.sku 
                AND sc.PERIOD = psd.YEAR 
                AND sc.CATEGORY_NAME = psd.CATEGORY
            WHERE sc.SUPPLIER_NAME != psd.primary_supplier
            GROUP BY sc.PERIOD, sc.CATEGORY_NAME, sc.SKU_NAME, sc.SUPPLIER_NAME
        )
        SELECT
            psd.YEAR,
            psd.CATEGORY,
            psd.primary_supplier,
            psd.sku,
            psd.total_quantity,
            psd.avg_unit_price,
            -- Multisourcing information
            scd.supplier_count,
            CASE 
                WHEN scd.supplier_count > 1 THEN 'MULTISOURCED'
                ELSE 'SINGLE_SOURCE'
            END AS sourcing_status,
            -- Alternate supplier information
            alt1.alternate_supplier AS best_alternate_supplier,
            alt1.alternate_price AS best_alternate_price,
            ROUND((psd.avg_unit_price - alt1.alternate_price) / psd.avg_unit_price * 100, 2) AS potential_savings_pct,
            alt2.alternate_supplier AS second_alternate_supplier,
            alt2.alternate_price AS second_alternate_price,
            -- Price comparison metrics
            CASE
                WHEN alt1.alternate_price < psd.avg_unit_price THEN 'BETTER_PRICE_AVAILABLE'
                WHEN alt1.alternate_price = psd.avg_unit_price THEN 'COMPETITIVE_PRICE'
                ELSE 'CURRENT_BEST_PRICE'
            END AS price_status
        FROM filtered_primary_data psd
        LEFT JOIN supplier_count_data scd ON psd.YEAR = scd.YEAR 
            AND psd.CATEGORY = scd.CATEGORY 
            AND psd.sku = scd.sku
        LEFT JOIN alternate_suppliers alt1 ON psd.YEAR = alt1.YEAR 
            AND psd.CATEGORY = alt1.CATEGORY 
            AND psd.sku = alt1.sku 
            AND alt1.price_rank = 1 
        LEFT JOIN alternate_suppliers alt2 ON psd.YEAR = alt2.YEAR 
            AND psd.CATEGORY = alt2.CATEGORY 
            AND psd.sku = alt2.sku 
            AND alt2.price_rank = 2
        where  scd.supplier_count>1
        and primary_supplier='{supplier_name}'    """
    batna = sf_client.fetch_dataframe(query)
    batna_data = batna.to_json(orient='records', date_format='iso')
    return batna_data
def get_zopa_details(
    sf_client: SnowflakeClient,
    supplier_name: str,
    category: str,
) -> list:
    """Fetch ZOPA details for a given supplier and category."""
    query = f"""
        WITH supplier_pricing_data AS (
            SELECT
                PERIOD AS YEAR,
                CATEGORY_NAME AS CATEGORY,
                SKU_NAME as sku,
                SUPPLIER_NAME,
                AVG(UNIT_PRICE) AS avg_unit_price,
                MIN(UNIT_PRICE) AS min_price,
                MAX(UNIT_PRICE) AS max_price,
                SUM(QUANTITY) AS total_quantity,
                COUNT(*) AS transaction_count
            FROM data.T_C_NEGOTIATION_FACTORY_T2
            where PERIOD='2025' and category='{category}'
            GROUP BY PERIOD, CATEGORY_NAME, SKU_NAME, SUPPLIER_NAME
        ),
        market_benchmarks AS (
            SELECT
                YEAR,
                CATEGORY,
                MATERIAL as sku,
                MIN(BENCHMARK_UNIT_PRICE) AS market_min_price,
                MAX(BENCHMARK_UNIT_PRICE) AS market_max_price,
                AVG(BENCHMARK_UNIT_PRICE) AS market_avg_price,
                PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY BENCHMARK_UNIT_PRICE) AS market_25th_percentile,
                PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY BENCHMARK_UNIT_PRICE) AS market_75th_percentile,
                COUNT(DISTINCT SUPPLIER) AS supplier_count
            FROM Data.T_C_WEB_PRICE_BENCHMARK
            where Year='2025' and category='{category}'
            GROUP BY YEAR, CATEGORY, sku
        ),
        supplier_negotiation_range AS (
            SELECT
                spd.*,
                -- Supplier's likely minimum acceptable price (cost floor estimate)
                CASE 
                    WHEN spd.min_price = spd.max_price THEN spd.min_price * 0.95  -- 5% margin if fixed price
                    ELSE spd.min_price * 0.98  -- 2% margin above historical minimum
                END AS supplier_reservation_price,
                
                -- Supplier's aspiration price (what they'd like to get)
                CASE 
                    WHEN spd.max_price > spd.avg_unit_price * 1.1 THEN spd.max_price
                    ELSE spd.avg_unit_price * 1.05  -- 5% above average
                END AS supplier_aspiration_price
            FROM supplier_pricing_data spd
        ),
        buyer_negotiation_range AS (
            SELECT
                mb.*,
                -- Buyer's maximum acceptable price (reservation price)
                CASE 
                    WHEN mb.market_75th_percentile > mb.market_avg_price * 1.2 THEN mb.market_avg_price * 1.15
                    ELSE mb.market_75th_percentile
                END AS buyer_reservation_price,
                
                -- Buyer's aspiration price (what they'd like to pay)
                CASE 
                    WHEN mb.market_min_price < mb.market_avg_price * 0.8 THEN mb.market_avg_price * 0.85
                    ELSE mb.market_25th_percentile
                END AS buyer_aspiration_price
            FROM market_benchmarks mb
        ),
        zopa_analysis AS (
            SELECT
                snr.YEAR,
                snr.CATEGORY,
                snr.sku,
                snr.SUPPLIER_NAME,
                snr.avg_unit_price AS current_price,
                snr.total_quantity,
                bnr.supplier_count,
                
                -- Supplier negotiation range
                snr.supplier_reservation_price,
                snr.supplier_aspiration_price,
                
                -- Buyer negotiation range
                bnr.buyer_aspiration_price,
                bnr.buyer_reservation_price,
                
                -- Market context
                bnr.market_min_price,
                bnr.market_max_price,
                bnr.market_avg_price,
                
                -- ZOPA calculation
                CASE 
                    WHEN snr.supplier_reservation_price <= bnr.buyer_reservation_price THEN 'ZOPA_EXISTS'
                    ELSE 'NO_ZOPA'
                END AS zopa_status,
                
                -- ZOPA range (if it exists)
                CASE 
                    WHEN snr.supplier_reservation_price <= bnr.buyer_reservation_price THEN snr.supplier_reservation_price
                    ELSE NULL
                END AS zopa_lower_bound,
                
                CASE 
                    WHEN snr.supplier_reservation_price <= bnr.buyer_reservation_price THEN bnr.buyer_reservation_price
                    ELSE NULL
                END AS zopa_upper_bound,
                
                -- Negotiation potential
                CASE 
                    WHEN snr.supplier_reservation_price <= bnr.buyer_reservation_price THEN 
                        ROUND((bnr.buyer_reservation_price - snr.supplier_reservation_price) / snr.avg_unit_price * 100, 2)
                    ELSE 0
                END AS negotiation_potential_pct,
                
                -- Recommended target price
                CASE 
                    WHEN snr.supplier_reservation_price <= bnr.buyer_reservation_price THEN 
                        ROUND((snr.supplier_reservation_price + bnr.buyer_reservation_price) / 2, 2)
                    ELSE snr.avg_unit_price
                END AS recommended_target_price,
                
                -- Negotiation difficulty assessment
                CASE 
                    WHEN snr.supplier_reservation_price <= bnr.buyer_reservation_price THEN
                        CASE 
                            WHEN (bnr.buyer_reservation_price - snr.supplier_reservation_price) / snr.avg_unit_price > 0.15 THEN 'EASY'
                            WHEN (bnr.buyer_reservation_price - snr.supplier_reservation_price) / snr.avg_unit_price > 0.05 THEN 'MODERATE'
                            ELSE 'DIFFICULT'
                        END
                    ELSE 'VERY_DIFFICULT'
                END AS negotiation_difficulty,
                
                -- Supplier power assessment
                CASE 
                    WHEN bnr.supplier_count = 1 THEN 'HIGH_SUPPLIER_POWER'
                    WHEN bnr.supplier_count <= 3 THEN 'MEDIUM_SUPPLIER_POWER'
                    ELSE 'LOW_SUPPLIER_POWER'
                END AS supplier_power,
                
                -- Current price position
                CASE 
                    WHEN snr.avg_unit_price <= bnr.buyer_aspiration_price THEN 'EXCELLENT_PRICE'
                    WHEN snr.avg_unit_price <= bnr.market_avg_price THEN 'GOOD_PRICE'
                    WHEN snr.avg_unit_price <= bnr.buyer_reservation_price THEN 'ACCEPTABLE_PRICE'
                    ELSE 'OVERPRICED'
                END AS current_price_assessment
            FROM supplier_negotiation_range snr
            JOIN buyer_negotiation_range bnr ON snr.YEAR = bnr.YEAR 
                AND snr.CATEGORY = bnr.CATEGORY 
                AND snr.sku = bnr.sku
        )
        SELECT
            YEAR,
            CATEGORY,
            sku,
            SUPPLIER_NAME,
            current_price,
            total_quantity,
            supplier_count,
            
            -- ZOPA Analysis
            zopa_status,
            zopa_lower_bound,
            zopa_upper_bound,
            recommended_target_price,
            negotiation_potential_pct,
            
            -- Negotiation Context
            negotiation_difficulty,
            supplier_power,
            current_price_assessment,
            
            -- Detailed Ranges (for advanced analysis)
            supplier_reservation_price,
            supplier_aspiration_price,
            buyer_aspiration_price,
            buyer_reservation_price,
            
            -- Market Context
            market_min_price,
            market_avg_price,
            market_max_price,
            
            -- Savings Potential
            ROUND((current_price - recommended_target_price) * total_quantity, 2) AS potential_annual_savings,
            
            -- Negotiation Strategy
            CASE 
                WHEN zopa_status = 'ZOPA_EXISTS' AND negotiation_difficulty = 'EASY' THEN 'AGGRESSIVE_NEGOTIATION'
                WHEN zopa_status = 'ZOPA_EXISTS' AND negotiation_difficulty = 'MODERATE' THEN 'COLLABORATIVE_NEGOTIATION'
                WHEN zopa_status = 'ZOPA_EXISTS' AND negotiation_difficulty = 'DIFFICULT' THEN 'CAREFUL_NEGOTIATION'
                WHEN zopa_status = 'NO_ZOPA' AND supplier_power = 'HIGH_SUPPLIER_POWER' THEN 'EXPLORE_ALTERNATIVES'
                WHEN zopa_status = 'NO_ZOPA' AND supplier_power != 'HIGH_SUPPLIER_POWER' THEN 'LEVERAGE_COMPETITION'
                ELSE 'MAINTAIN_STATUS_QUO'
            END AS recommended_strategy

        FROM zopa_analysis
        WHERE SUPPLIER_NAME = '{supplier_name}'
        ORDER BY 
            potential_annual_savings DESC,
            negotiation_potential_pct DESC;
    """
    zopa_data = sf_client.fetch_dataframe(query)
    zopa_json = zopa_data.to_json(orient='records', date_format='iso')
    return zopa_json

def weighted_average(group: pd.DataFrame, term: str, average_term: str) -> float:
    """
    calculate weighted average for a group.
    Args:
        group (pd.DataFrame): group of data
    Returns:
        (float): weighted average
    """
    spend_sum = group[average_term].sum()
    if spend_sum == 0:
        return 0
    return (group[average_term] * group[term]).sum() / spend_sum

def get_all_skus(sf_client: SnowflakeClient, supplier_name: str, category: str) -> list[dict]:
    query = f"""
        SELECT sku_id,
            sku_name,
            unit_price,
            quantity,
            unit_of_measurement,
            spend_ytd,
            REPORTING_CURRENCY,
            period
        FROM Data.T_C_NEGOTIATION_FACTORY_T2
        WHERE category_name = '{category}'
        AND period = (SELECT MAX(PERIOD) FROM Data.T_C_NEGOTIATION_FACTORY_T2)
        AND supplier_name = '{supplier_name}'
        ORDER BY spend_ytd DESC
    """
    try:
        sku_data = sf_client.fetch_dataframe(query)
        sku_data.rename(columns={"REPORTING_CURRENCY": "currency_symbol"}, inplace=True)
        sku_data['currency_symbol'] = sku_data['currency_symbol'].map(
            lambda x: CurrencySymbol[x].value if x in CurrencySymbol.__members__ else " "
        )
        sku_data.columns = sku_data.columns.str.lower()
        if not sku_data.empty:
            sku_data = (
                sku_data.groupby(["sku_id", "sku_name", "currency_symbol"], as_index=False)
                .agg({
                    "quantity": "sum",
                    "spend_ytd": "sum",
                    "unit_price": lambda x: weighted_average(
                        sku_data.loc[x.index], term="unit_price", average_term="quantity"
                    ),
                    "unit_of_measurement": lambda x: x.dropna().loc[x != ""].mode().iat[0] if not x.dropna().loc[x != ""].empty else ""
                })
            )
            sku_data.rename(columns={
                "sku_id": "id",
                "sku_name": "name",
                "unit_of_measurement": "uom",
                "spend_ytd": "spend",
            }, inplace=True)
            sku_data.sort_values(by="spend", ascending=False, inplace=True)
            sku_data.reset_index(drop=True, inplace=True)
            return sku_data.to_json(orient='records', date_format='iso')
        else:
            return "[]"
    except Exception:
        return "[]"
