def top_suppliers_with_most_opportunity(category, sf_client):
    sql = f"""
        SELECT 
            SUPPLIER,
            SUM(KPI_VALUE) AS TOTAL_OPPORTUNITY
        FROM 
            data.t_c_total_savings_opportunity_frontend
        WHERE 
            YEAR = (SELECT MAX(YEAR) FROM data.t_c_total_savings_opportunity_frontend)
            AND CATEGORY = '{category}' AND KPI_NAME = 'Total saving opportunity'
        GROUP BY 
            SUPPLIER
        ORDER BY 
            TOTAL_OPPORTUNITY DESC
        LIMIT 10;
        """
    result = sf_client.fetch_dataframe(sql)
    return [result.to_dict(orient='records'),sql]

def supplier_opportunity_breakdown(supplier, category, sf_client):
    sql = f"""
        SELECT 
            SUPPLIER,
            KPI_NAME,
            SUM(KPI_VALUE) AS KPI_OPPORTUNITY
        FROM 
            data.t_c_total_savings_opportunity_frontend
        WHERE 
            YEAR = (SELECT MAX(YEAR) FROM data.t_c_total_savings_opportunity_frontend)
            AND SUPPLIER = '{supplier}'
            AND CATEGORY = '{category}'
            AND KPI_NAME NOT IN ('Spends', 'Total saving opportunity','Supplier Consolidation')
        GROUP BY 
            SUPPLIER, KPI_NAME
        ORDER BY 
            SUPPLIER, KPI_NAME;

        """
    result = sf_client.fetch_dataframe(sql)
    return [result.to_dict(orient='records'),sql]

def supplier_top_opportunity_materials(supplier, category, sf_client):
    sql = f"""
        SELECT 
            MATERIAL,
            SUM(KPI_VALUE) AS TOTAL_OPPORTUNITY
        FROM 
            data.t_c_total_savings_opportunity_frontend
        WHERE 
            SUPPLIER = '{supplier}'
            AND YEAR = (SELECT MAX(YEAR) FROM data.t_c_total_savings_opportunity_frontend)
            AND CATEGORY = '{category}' AND KPI_NAME = 'Total saving opportunity'
        GROUP BY 
            MATERIAL
        ORDER BY 
            TOTAL_OPPORTUNITY DESC
        LIMIT 5;

        """
    result = sf_client.fetch_dataframe(sql)
    return [result.to_dict(orient='records'),sql]

def supplier_top_opportunity_plants(supplier, category, sf_client):
    sql = f"""
        SELECT 
            PLANT,
            SUM(KPI_VALUE) AS TOTAL_OPPORTUNITY
        FROM 
            data.t_c_total_savings_opportunity_frontend
        WHERE 
            SUPPLIER = '{supplier}'
            AND YEAR = (SELECT MAX(YEAR) FROM data.t_c_total_savings_opportunity_frontend)
            AND CATEGORY = '{category}' AND KPI_NAME = 'Total saving opportunity'
        GROUP BY 
            PLANT
        ORDER BY 
            TOTAL_OPPORTUNITY DESC
        LIMIT 5;

        """
    result = sf_client.fetch_dataframe(sql)
    return [result.to_dict(orient='records'),sql]


def supplier_top_opportunity_regions(supplier, category, sf_client):
    sql = f"""
        SELECT 
            COUNTRY,
            SUM(KPI_VALUE) AS TOTAL_OPPORTUNITY
        FROM 
            data.t_c_total_savings_opportunity_frontend
        WHERE 
            SUPPLIER = '{supplier}'
            AND YEAR = (SELECT MAX(YEAR) FROM data.t_c_total_savings_opportunity_frontend)
            AND CATEGORY = '{category}' AND KPI_NAME = 'Total saving opportunity'
        GROUP BY 
            COUNTRY
        ORDER BY 
            TOTAL_OPPORTUNITY DESC
        LIMIT 5;

        """
    result = sf_client.fetch_dataframe(sql)
    return [result.to_dict(orient='records'),sql]


def total_spend_by_supplier(supplier, category, sf_client):
    sql = f"""
    SELECT 
        SUPPLIER,
        SUM(TOTAL_SPEND)
    FROM 
        data.NEGO_SUPPLIER_MASTER
    WHERE 
        YEAR = (SELECT MAX(YEAR) FROM data.NEGO_SUPPLIER_MASTER) AND SUPPLIER = '{supplier}' AND CATEGORY = '{category}'
    GROUP BY 
        SUPPLIER
    """
    result = sf_client.fetch_dataframe(sql)
    return [result.to_dict(orient='records'),sql]

def category_supplier_stats(category, sf_client):
    sql = f"""
    SELECT 
        CATEGORY,
        COUNT(DISTINCT SUPPLIER_ID) AS SUPPLIER_COUNT,
        SUM(SPEND_YTD) AS TOTAL_SPEND,
        SUM(SINGLE_SOURCE_SPEND_YTD) AS SINGLE_SOURCE_SPEND
    FROM 
        data.NEGO_SUPPLIER_MASTER
    WHERE 
        YEAR = (SELECT MAX(YEAR) FROM data.NEGO_SUPPLIER_MASTER) AND CATEGORY = '{category}'
    GROUP BY 
        CATEGORY
    ORDER BY 
        TOTAL_SPEND DESC;
    """
    result = sf_client.fetch_dataframe(sql)
    return [result.to_dict(orient='records'),sql]

def single_source_spend_by_supplier(supplier, category, sf_client):
    sql = f"""
    SELECT 
        YEAR,
        SUPPLIER,
        SUM(SINGLE_SOURCE_SPEND_YTD) AS SINGLE_SOURCE_SPEND
    FROM 
        data.NEGO_SUPPLIER_MASTER
    WHERE 
        YEAR = (SELECT MAX(YEAR) FROM data.NEGO_SUPPLIER_MASTER) AND SUPPLIER = '{supplier}' AND CATEGORY = '{category}'
    GROUP BY
        YEAR,SUPPLIER
    ORDER BY 
        SINGLE_SOURCE_SPEND DESC
    """
    result = sf_client.fetch_dataframe(sql)
    return [result.to_dict(orient='records'),sql]


def suppliers_with_yoy_increase_in_single_source_spend(category, sf_client):
    sql = f"""
    SELECT 
        SUPPLIER,
        SUM(SINGLE_SOURCE_SPEND_LAST_YEAR) AS SINGLE_SOURCE_SPEND_LAST_YEAR,
        SUM(SINGLE_SOURCE_SPEND_YTD) AS SINGLE_SOURCE_SPEND,
        (SUM(SINGLE_SOURCE_SPEND_YTD) - SUM(SINGLE_SOURCE_SPEND_LAST_YEAR)) AS YOY_GROWTH
    FROM 
        data.NEGO_SUPPLIER_MASTER
    WHERE 
        YEAR = (SELECT MAX(YEAR) FROM data.NEGO_SUPPLIER_MASTER) 
        AND CATEGORY = '{category}'
        AND SINGLE_SOURCE_SPEND_LAST_YEAR IS NOT NULL
    GROUP BY
        SUPPLIER
    ORDER BY 
        YOY_GROWTH DESC
    LIMIT 10;

    """
    result = sf_client.fetch_dataframe(sql)
    return [result.to_dict(orient='records'),sql]


def top_tail_spend_suppliers(category, sf_client):
    sql = f"""
    WITH supplier_spend AS (
        SELECT 
            SUPPLIER,
            SUM(SPEND_YTD) AS SPEND
        FROM 
            DATA.NEGO_SUPPLIER_MASTER
        WHERE 
            YEAR = (SELECT MAX(YEAR) FROM DATA.NEGO_SUPPLIER_MASTER)
            AND CATEGORY = '{category}'
        GROUP BY
            SUPPLIER
    ),
    supplier_ranked AS (
        SELECT 
            SUPPLIER,
            SPEND,
            SUM(SPEND) OVER (ORDER BY SPEND DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS CUMULATIVE_SPEND,
            SUM(SPEND) OVER () AS TOTAL_SPEND
        FROM 
            supplier_spend
    )
    SELECT 
        SUPPLIER,
        SPEND
    FROM 
        supplier_ranked
    WHERE 
        CUMULATIVE_SPEND / TOTAL_SPEND > 0.8
    ORDER BY 
        SPEND DESC
    LIMIT 10;
    """
    result = sf_client.fetch_dataframe(sql)
    return [result.to_dict(orient='records'),sql]



