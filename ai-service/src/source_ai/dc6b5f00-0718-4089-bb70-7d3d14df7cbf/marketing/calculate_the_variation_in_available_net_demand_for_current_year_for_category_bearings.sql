WITH
    CURRENT_DATES AS (
        SELECT
            MIN(TO_DATE (VDP.DIM_DATE, 'YYYYMMDD')) AS MIN_DATE,
            MAX(TO_DATE (VDP.DIM_DATE, 'YYYYMMDD')) AS MAX_DATE
        FROM
            DATA.VT_DIM_PERIOD AS VDP
        WHERE
            YEAR (TO_DATE (VDP.DIM_DATE, 'YYYYMMDD')) = YEAR (CURRENT_DATE)
            AND QUARTER (TO_DATE (VDP.DIM_DATE, 'YYYYMMDD')) = QUARTER (CURRENT_DATE)
    ),
    CURRENT_QUARTER_DATA AS (
        SELECT
            YEAR (TO_DATE (DIM_DATE, 'YYYYMMDD')) AS YEAR,
            QUARTER (TO_DATE (DIM_DATE, 'YYYYMMDD')) AS QUARTER,
            TXT_CATEGORY AS CATEGORY,
            TXT_BEROE_SUBCATEGORY AS BEROE_CATEGORY,
            TXT_CRITERIA AS CRITERIA,
            MAX(MES_VALUE) AS CURRENT_NET_DEMAND
        FROM
            DATA.T_C_MARKET_ANALYSIS
        WHERE
            LOWER(TXT_CRITERIA) LIKE LOWER('%Available Net Demand%')
            AND LOWER(TXT_LOCATION) = LOWER('Global')
            AND TO_DATE (DIM_DATE, 'YYYYMMDD') >= (
                SELECT
                    MIN_DATE
                FROM
                    CURRENT_DATES
            )
            AND TO_DATE (DIM_DATE, 'YYYYMMDD') <= (
                SELECT
                    MAX_DATE
                FROM
                    CURRENT_DATES
            )
            AND LOWER(TXT_CATEGORY) = LOWER('Bearings')
        GROUP BY
            YEAR (TO_DATE (DIM_DATE, 'YYYYMMDD')),
            QUARTER (TO_DATE (DIM_DATE, 'YYYYMMDD')),
            TXT_BEROE_SUBCATEGORY,
            TXT_CATEGORY,
            TXT_CRITERIA
    ),
    PREVIOUS_QUARTER_DATA AS (
        SELECT
            YEAR (TO_DATE (DIM_DATE, 'YYYYMMDD')) AS YEAR,
            QUARTER (TO_DATE (DIM_DATE, 'YYYYMMDD')) AS QUARTER,
            TXT_CATEGORY AS CATEGORY,
            TXT_BEROE_SUBCATEGORY AS BEROE_CATEGORY,
            TXT_CRITERIA AS CRITERIA,
            MAX(MES_VALUE) AS PREVIOUS_NET_DEMAND
        FROM
            DATA.T_C_MARKET_ANALYSIS
        WHERE
            LOWER(TXT_CRITERIA) LIKE LOWER('%Available Net Demand%')
            AND LOWER(TXT_LOCATION) = LOWER('Global')
            AND TO_DATE (DIM_DATE, 'YYYYMMDD') >= (
                SELECT
                    DATEADD (MONTH, -3, MIN_DATE)
                FROM
                    CURRENT_DATES
            )
            AND TO_DATE (DIM_DATE, 'YYYYMMDD') <= (
                SELECT
                    DATEADD (MONTH, -3, MAX_DATE)
                FROM
                    CURRENT_DATES
            )
            AND LOWER(TXT_CATEGORY) = LOWER('Bearings')
        GROUP BY
            YEAR (TO_DATE (DIM_DATE, 'YYYYMMDD')),
            QUARTER (TO_DATE (DIM_DATE, 'YYYYMMDD')),
            TXT_BEROE_SUBCATEGORY,
            TXT_CATEGORY,
            TXT_CRITERIA
    )
SELECT
    CQD.YEAR,
    CQD.QUARTER,
    CQD.CATEGORY,
    CQD.BEROE_CATEGORY,
    CQD.CRITERIA,
    (CURRENT_NET_DEMAND),
    PREVIOUS_NET_DEMAND,
    ROUND(
        (
            CAST(CURRENT_NET_DEMAND AS DECIMAL) - CAST(PREVIOUS_NET_DEMAND AS DECIMAL)
        ) / CAST(PREVIOUS_NET_DEMAND AS DECIMAL),
        2
    ) AS VARIATION_NET_DEMAND,
    ROUND(
        (
            (
                CAST(CURRENT_NET_DEMAND AS DECIMAL) - CAST(PREVIOUS_NET_DEMAND AS DECIMAL)
            ) / CAST(PREVIOUS_NET_DEMAND AS DECIMAL)
        ) * 100,
        2
    ) AS VARIATION_NET_DEMAND_PERCENTAGE
FROM
    CURRENT_QUARTER_DATA CQD
    JOIN PREVIOUS_QUARTER_DATA PQD ON CQD.CRITERIA = PQD.CRITERIA
    AND CQD.CATEGORY = PQD.CATEGORY
    AND CQD.BEROE_CATEGORY = PQD.BEROE_CATEGORY