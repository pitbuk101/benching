def get_supplier_ranking(supplier, category, sf_client):
    sql = f"""
    Select * from (SELECT 
        SUPPLIER_NAME,
        PERIOD,
        CATEGORY_NAME,
        SUM(SPEND_YTD) AS TOTAL_SPEND_ON_SUPPLIER,
        RANK() OVER (ORDER BY SUM(SPEND_YTD) DESC) AS SUPPLIER_RANK,
        COUNT(DISTINCT SUPPLIER_NAME) OVER () AS TOTAL_SUPPLIERS,
        (SUM(SPEND_YTD) / SUM(SUM(SPEND_YTD)) OVER ()) * 100 AS PERCENT_OF_TOTAL_SPEND
    FROM DATA.T_C_NEGOTIATION_FACTORY_T2
    WHERE CATEGORY_NAME = '{category}'
    AND PERIOD = (SELECT MAX(PERIOD) FROM DATA.T_C_NEGOTIATION_FACTORY_T2)
    AND SPEND_YTD > 0
    GROUP BY SUPPLIER_NAME, CATEGORY_NAME, PERIOD
    ORDER BY TOTAL_SPEND_ON_SUPPLIER DESC) where SUPPLIER_NAME = '{supplier}'
    """
    result = sf_client.fetch_dataframe(sql)
    return result.to_dict(orient='records')


def get_top_materials(supplier, category, sf_client, limit=3):
    sql = f"""
    SELECT SUPPLIER_NAME, SKU_NAME, PERIOD, SUM(SPEND_YTD) AS TOTAL_SPEND
    FROM DATA.T_C_NEGOTIATION_FACTORY_T2
    WHERE CATEGORY_NAME = '{category}'
      AND SUPPLIER_NAME = '{supplier}'
      AND PERIOD = (SELECT MAX(PERIOD) FROM DATA.T_C_NEGOTIATION_FACTORY_T2)
    GROUP BY SUPPLIER_NAME, SKU_NAME, PERIOD
    ORDER BY TOTAL_SPEND DESC
    LIMIT {limit}
    """
    result = sf_client.fetch_dataframe(sql)
    return result.to_dict(orient='records')


def get_top_business_units(supplier, category, sf_client, limit=3):
    sql = f"""
    SELECT YEAR, CATEGORY AS CATEGORY_NAME, SUPPLIER AS SUPPLIER_NAME, PLANT AS BUSINESS_UNIT, SUM(KPI_VALUE) AS SPEND
    FROM DATA.T_C_TOTAL_SAVINGS_OPPORTUNITY_FRONTEND
    WHERE KPI_NAME = 'Spends'
      AND CATEGORY = '{category}'
      AND SUPPLIER = '{supplier}'
      AND YEAR = (SELECT MAX(PERIOD) FROM DATA.T_C_NEGOTIATION_FACTORY_T2)
    GROUP BY YEAR, CATEGORY_NAME, SUPPLIER_NAME, BUSINESS_UNIT
    ORDER BY SPEND DESC
    LIMIT {limit}
    """
    result = sf_client.fetch_dataframe(sql)
    return result.to_dict(orient='records')


def get_top_payment_terms(supplier, category, sf_client, limit=3):
    sql = f"""
    SELECT SUPPLIER_NAME,PERIOD,CATEGORY_NAME,PAYMENT_TERMS,SUM(SPEND_YTD) AS TOTAL_SPEND,
	   (SUM(SPEND_YTD) / SUM(SUM(SPEND_YTD)) OVER ()) * 100 AS PERCENTAGE
    FROM DATA.T_C_NEGOTIATION_FACTORY_T2
    WHERE CATEGORY_NAME = '{category}'
    AND SUPPLIER_NAME = '{supplier}'
    AND PERIOD = (SELECT MAX(PERIOD) FROM DATA.T_C_NEGOTIATION_FACTORY_T2)
    AND SPEND_YTD > 0
    GROUP BY SUPPLIER_NAME,PERIOD,PAYMENT_TERMS,CATEGORY_NAME,PAYMENT_TERMS
    ORDER BY TOTAL_SPEND DESC
    LIMIT {limit};
    """
    result = sf_client.fetch_dataframe(sql)
    return result.to_dict(orient='records')


def get_spend_without_po(supplier, category, sf_client):
    sql = f"""
    SELECT SUPPLIER_NAME,PERIOD,CATEGORY_NAME,SUM(SPEND_WITHOUT_PO_YTD) AS SPEND_WITHOUT_PO,
	   (SUM(SPEND_WITHOUT_PO_YTD) / SUM(SPEND_YTD)) * 100 AS PERCENTAGE
    FROM DATA.T_C_NEGOTIATION_FACTORY_T2
    WHERE CATEGORY_NAME = '{category}'
    AND SUPPLIER_NAME = '{supplier}'
    AND PERIOD = (SELECT MAX(PERIOD) FROM DATA.T_C_NEGOTIATION_FACTORY_T2)
    AND SPEND_YTD > 0
    GROUP BY SUPPLIER_NAME,PERIOD,CATEGORY_NAME;
    """
    result = sf_client.fetch_dataframe(sql)
    return result.to_dict(orient='records')


def get_spend_without_material_reference(supplier, category, sf_client):
    sql = f"""
    SELECT
    PERIOD,
    SUPPLIER_NAME,
    CATEGORY_NAME,
    SUM(SPEND_YTD) AS SPEND_WITHOUT_MATERIAL_REFERENCE,
    (SUM(SPEND_YTD) / (SELECT SUM(SPEND_YTD) FROM DATA.T_C_NEGOTIATION_FACTORY_T2 WHERE SUPPLIER_NAME = '{supplier}' AND CATEGORY_NAME='{category}' AND PERIOD = (SELECT MAX(PERIOD) FROM DATA.T_C_NEGOTIATION_FACTORY_T2 WHERE SKU_NAME is NULL))) * 100 AS PERCENTAGE
    FROM DATA.T_C_NEGOTIATION_FACTORY_T2
    WHERE SUPPLIER_NAME = '{supplier}'
    AND CATEGORY_NAME='{category}'
    AND PERIOD = (SELECT MAX(PERIOD) FROM DATA.T_C_NEGOTIATION_FACTORY_T2)
    AND SKU_NAME IS NULL
    AND SPEND_YTD > 0
    GROUP BY PERIOD,
    SUPPLIER_NAME,
    CATEGORY_NAME
    """
    result = sf_client.fetch_dataframe(sql)
    return result.to_dict(orient='records')


def get_spend(supplier, category, sf_client):
    sql = f"""
            SELECT * FROM DATA.T_C_NEGOTIATION_FACTORY_T2
            WHERE CATEGORY_NAME = '{category}'
            AND SUPPLIER_NAME = '{supplier}'
            AND PERIOD IN (
                (SELECT MAX(PERIOD) FROM DATA.T_C_NEGOTIATION_FACTORY_T2),
                (SELECT MAX(PERIOD) - 1 FROM DATA.T_C_NEGOTIATION_FACTORY_T2)
            )
        """
    result = sf_client.fetch_dataframe(sql)
    return result.to_dict(orient='records')


def get_price_volume(supplier, material, category, sf_client):
    sql = f"""
    SELECT
        Supplier_name,
        SKU_NAME,
        PERIOD AS YEAR,
        category_name,
        (SUM(SPEND_YTD) - SUM(SPEND_LAST_YEAR)) AS spend_variance_absolute,
        (SUM(UNIT_PRICE) - SUM(UNIT_PRICE_LAST_YEAR)) AS price_variance_absolute,
        (SUM(QUANTITY) - SUM(QUANTITY_LAST_YEAR)) AS quantity_variance_absolute,
        CASE WHEN SUM(SPEND_LAST_YEAR) != 0 THEN ((SUM(SPEND_YTD) - SUM(SPEND_LAST_YEAR)) / SUM(SPEND_LAST_YEAR)) * 100 ELSE NULL END AS spend_variance_percentage,
        CASE WHEN SUM(UNIT_PRICE_LAST_YEAR) != 0 THEN ((SUM(UNIT_PRICE) - SUM(UNIT_PRICE_LAST_YEAR)) / SUM(UNIT_PRICE_LAST_YEAR)) * 100 ELSE NULL END AS price_variance_percentage,
        CASE WHEN SUM(Quantity_LAST_YEAR) != 0 THEN ((SUM(QUANTITY) - SUM(Quantity_LAST_YEAR)) / SUM(Quantity_LAST_YEAR)) * 100 ELSE NULL END AS quantity_variance_percentage
    FROM DATA.T_C_NEGOTIATION_FACTORY_T2
    WHERE supplier_name = '{supplier}'
    AND category_name = '{category}'
    AND SKU_NAME IN ('{material}')
    AND SPEND_YTD > 0 AND SPEND_LAST_YEAR != 0
    AND Period = (SELECT MAX(PERIOD) FROM DATA.T_C_NEGOTIATION_FACTORY_T2)
    GROUP BY Supplier_name, category_name, SKU_NAME, YEAR
    """
    result = sf_client.fetch_dataframe(sql)
    return result.to_dict(orient='records')


def get_single_multi_source(supplier, material,category, sf_client):
    sql = f"""
    WITH Avg_unit_price AS (
        SELECT 
            PERIOD AS YEAR,
            SKU_NAME, 
            AVG(UNIT_PRICE) AS AVERAGE_UNIT_PRICE_ACROSS_SUPPLIERS
        FROM DATA.T_C_NEGOTIATION_FACTORY_T2
        WHERE SKU_NAME IN ('{material}') 
            AND CATEGORY_NAME = '{category}'
            AND PERIOD = (SELECT MAX(PERIOD) FROM DATA.T_C_NEGOTIATION_FACTORY_T2)
        GROUP BY SKU_NAME, YEAR
    )
    SELECT
        t1.Supplier_name,
        t1.SKU_NAME,
        t2.YEAR,
        CASE 
            WHEN SPEND_SINGLE_SOURCE_YTD IS NOT NULL AND SPEND_SINGLE_SOURCE_YTD != 0 THEN 'SINGLE SOURCED'
            WHEN MULTI_SOURCE_SPEND_YTD IS NOT NULL AND MULTI_SOURCE_SPEND_YTD != 0 THEN 'MULTI SOURCED'
            ELSE NULL
        END AS SOURCED_TYPE,
        CASE 
            WHEN SPEND_SINGLE_SOURCE_YTD IS NOT NULL THEN SPEND_SINGLE_SOURCE_YTD
            WHEN MULTI_SOURCE_SPEND_YTD IS NOT NULL THEN MULTI_SOURCE_SPEND_YTD
            ELSE NULL
        END AS CURRENT_YEAR_SPEND,
        t1.UNIT_PRICE,
        CASE 
            WHEN MULTI_SOURCE_SPEND_YTD IS NOT NULL THEN t2.AVERAGE_UNIT_PRICE_ACROSS_SUPPLIERS
            ELSE NULL
        END AS AVERAGE_UNIT_PRICE_ACROSS_SUPPLIERS
    FROM DATA.T_C_NEGOTIATION_FACTORY_T2 t1
    JOIN Avg_unit_price t2 
        ON t1.SKU_NAME = t2.SKU_NAME
    WHERE t1.PERIOD = (SELECT MAX(PERIOD) FROM DATA.T_C_NEGOTIATION_FACTORY_T2)
        AND t1.SPEND_YTD IS NOT NULL
        AND t1.CATEGORY_NAME = '{category}'
        AND t1.SKU_NAME IN ('{material}')
        AND t1.SUPPLIER_NAME = '{supplier}'

    """
    result = sf_client.fetch_dataframe(sql)
    return result.to_dict(orient='records')

