WITH FilteredInvoicePositions AS (
    SELECT 
        DIM_INCOTERM, 
        CAST(COALESCE(MES_SPEND_CURR_1, 0) AS REAL) AS MES_SPEND_CURR_1
    FROM 
        Fact invoice position
    WHERE 
 CAST(COALESCE(MES_SPEND_CURR_1, 0) AS REAL) > 0
),
FilteredInvoicePositionsExcludingNegativeOne AS (
    SELECT 
        DIM_INCOTERM, 
        MES_SPEND_CURR_1
    FROM 
        Fact invoice position
    WHERE 
        DIM_INCOTERM != '-1'
        AND CAST(COALESCE(MES_SPEND_CURR_1, 0) AS REAL) > 0
)
SELECT 
    COUNT(DIM_INCOTERM) AS IncotermCount
FROM 
    FilteredInvoicePositionsExcludingNegativeOne;