def top_single_sourced_materials(supplier,category,sf_client):
    sql = f"""
    SELECT
    PERIOD,
    CATEGORY_NAME,
    SUPPLIER_NAME,
    SKU_NAME,
    SUM(SPEND_SINGLE_SOURCE_YTD) AS SPEND_ON_SINGLE_SOURCE_MATERIAL,
    FROM
        data.t_c_negotiation_factory_t2
    WHERE
        SUPPLIER_NAME ='{supplier}'
        AND PERIOD = (SELECT MAX(PERIOD) from DATA.T_C_NEGOTIATION_FACTORY_T2)
        AND SPEND_SINGLE_SOURCE_YTD > 0
        AND CATEGORY_NAME = '{category}'
    GROUP BY
        SKU_NAME, CATEGORY_NAME, SUPPLIER_NAME,PERIOD
    ORDER BY
        SPEND_ON_SINGLE_SOURCE_MATERIAL DESC
    LIMIT 3;
    """

    result = sf_client.fetch_dataframe(sql)
    result = result.to_dict(orient='records')

    return result


def spend_increase_yoy_on_supplier(supplier,category,sf_client):
    sql = f"""
    WITH current_year_cte AS (
        SELECT MAX(TO_NUMBER(PERIOD)) AS year_now
        FROM DATA.T_C_NEGOTIATION_FACTORY_T2
    ),
    spend_summary AS (
        SELECT
            SUPPLIER_NAME,
            CATEGORY_NAME,
            SUM(CASE 
                    WHEN TO_NUMBER(PERIOD) = (SELECT year_now - 1 FROM current_year_cte) 
                    THEN SPEND_LAST_YEAR 
                    ELSE 0 
                END) AS total_spend_last_year,
            SUM(CASE 
                    WHEN TO_NUMBER(PERIOD) = (SELECT year_now FROM current_year_cte) 
                    THEN SPEND_YTD 
                    ELSE 0 
                END) AS total_spend_ytd
        FROM
            data.t_c_negotiation_factory_t2
        WHERE
            SUPPLIER_NAME = '{supplier}'
            AND CATEGORY_NAME = '{category}'
            AND TO_NUMBER(PERIOD) IN (
                (SELECT year_now FROM current_year_cte),
                (SELECT year_now - 1 FROM current_year_cte)
            )
        GROUP BY
            SUPPLIER_NAME,
            CATEGORY_NAME
    )
    SELECT
        SUPPLIER_NAME,
        CATEGORY_NAME,
        total_spend_last_year,
        total_spend_ytd,
        total_spend_ytd - total_spend_last_year AS absolute_change_eur,
        ROUND(
            ((total_spend_ytd - total_spend_last_year) / NULLIF(total_spend_last_year, 0)) * 100,
            2
        ) AS percent_change
    FROM
        spend_summary;

    """

    result = sf_client.fetch_dataframe(sql)
    result = result.to_dict(orient='records')

    return result



def get_single_source_data(supplier,category,year_master_subquery,sf_client):
    sql = f"""
    SELECT SUM(SINGLE_SOURCE_SPEND_YTD) AS SINGLE_SOURCE_SPEND,
    SUM(SPEND_YTD) AS TOTAL_SPEND_YTD,
    ((SUM(SINGLE_SOURCE_SPEND_YTD)*100)/ SUM(SPEND_YTD)) AS SINGLE_SOURCE_SPEND_PERCENTAGE_OF_TOTAL_SPEND,
    YEAR
    FROM DATA.NEGO_SUPPLIER_MASTER
    WHERE SUPPLIER = '{supplier}'
    AND CATEGORY = '{category}'
    AND YEAR = {year_master_subquery}
    GROUP BY YEAR
    """

    result = sf_client.fetch_dataframe(sql)
    result = result.to_dict(orient='records')

    return result



def get_high_spend_invoice_risk(supplier,category,year_master_subquery,sf_client):
    sql = f"""
    WITH Category_Avg AS (
            SELECT 
                SUM(SPEND_YTD) AS TOTAL_SPEND,
                SUM(INVOICE_COUNT_YTD) AS TOTAL_INVOICES,
                SUM(SPEND_YTD) / NULLIF(SUM(INVOICE_COUNT_YTD), 0) AS CATEGORY_AVG_SPEND
            FROM DATA.NEGO_SUPPLIER_MASTER
            WHERE CATEGORY = '{category}'
            AND YEAR = {year_master_subquery}
            AND INVOICE_COUNT_YTD > 0
        )

        SELECT 
            SM.SUPPLIER,
            SM.YEAR,
            SUM(SM.SPEND_YTD) AS SPEND_YTD,
            SUM(SM.INVOICE_COUNT_YTD) AS INVOICE_COUNT_YTD,
            SUM(SM.SPEND_YTD) / NULLIF(SUM(SM.INVOICE_COUNT_YTD), 0) AS SPEND_PER_INVOICE,
            CA.CATEGORY_AVG_SPEND
        FROM DATA.NEGO_SUPPLIER_MASTER SM
        CROSS JOIN Category_Avg CA
        WHERE SM.CATEGORY = '{category}'
        AND SM.SUPPLIER = '{supplier}'
        AND SM.YEAR = {year_master_subquery}
        AND SM.INVOICE_COUNT_YTD > 0
        GROUP BY SM.SUPPLIER, SM.YEAR, CA.CATEGORY_AVG_SPEND;

    """

    result = sf_client.fetch_dataframe(sql)
    result = result.to_dict(orient='records')

    return result


def get_multi_spend_drop_risk(supplier,category,year_master_subquery,sf_client):
    sql = f"""
    SELECT SUPPLIER,
        YEAR,
        SUM(MULTI_SOURCE_SPEND_LAST_YEAR) AS MULTI_SOURCE_SPEND_LAST_YEAR,
        SUM(MULTI_SOURCE_SPEND_YTD) AS MULTI_SOURCE_SPEND_YTD,
        SUM(MULTI_SOURCE_SPEND_LAST_YEAR) - SUM(MULTI_SOURCE_SPEND_YTD) AS DROP_IN_MULTI_SOURCE_SPEND
    FROM DATA.NEGO_SUPPLIER_MASTER
    WHERE CATEGORY = '{category}'
    AND SUPPLIER = '{supplier}'
    AND YEAR = {year_master_subquery}
    AND MULTI_SOURCE_SPEND_LAST_YEAR > MULTI_SOURCE_SPEND_YTD
    GROUP BY SUPPLIER, YEAR

    """

    result = sf_client.fetch_dataframe(sql)
    result = result.to_dict(orient='records')

    return result
