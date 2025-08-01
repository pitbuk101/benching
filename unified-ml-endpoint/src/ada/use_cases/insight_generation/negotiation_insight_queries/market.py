def get_market_data(supplier,material, category, sf_client):
    sql = f"""
        WITH YEAR_CHANGE AS (
            SELECT
                    YEAR,
                    CATEGORY,
                    AVG(CHANGE_IN_MARKET_PRICE_PERCENTAGE) AS CHANGE_IN_MARKET_PRICE_PERCENTAGE
            FROM DATA.SKU_PRICE_COMPARISON
            WHERE YEAR = YEAR = (SELECT MAX(YEAR) FROM DATA.SKU_PRICE_COMPARISON)
            GROUP BY YEAR,CATEGORY
        )
        SELECT
            SPC.YEAR,
            SPC.CATEGORY,
            SUPPLIER,
            SKU,
            AVG(CHANGE_IN_SKU_PRICE_PERCENTAGE) AS CHANGE_IN_SKU_PRICE_PERCENTAGE,
            YC.CHANGE_IN_MARKET_PRICE_PERCENTAGE
        FROM DATA.SKU_PRICE_COMPARISON SPC
        JOIN YEAR_CHANGE YC
        ON SPC.YEAR = YC.YEAR AND SPC.CATEGORY = YC.CATEGORY
        WHERE
            SUPPLIER = '{supplier}'
            AND SKU IN ('{material}')
            AND SPC.CATEGORY = '{category}'
            AND SPC.YEAR = (SELECT MAX(YEAR) FROM DATA.SKU_PRICE_COMPARISON)
        GROUP BY SPC.YEAR, SUPPLIER,SKU,SPC.CATEGORY,YC.CHANGE_IN_MARKET_PRICE_PERCENTAGE
        ORDER BY SKU ;
        """
    result = sf_client.fetch_dataframe(sql)
    return result.to_dict(orient='records')