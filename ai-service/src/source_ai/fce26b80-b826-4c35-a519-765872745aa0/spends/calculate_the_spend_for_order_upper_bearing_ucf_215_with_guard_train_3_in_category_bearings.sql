WITH OrderSpend AS (
    SELECT 
        o.TXT_ORDER_POSITION_LONG, 
        SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
    FROM 
        Fact invoice position fip
    LEFT OUTER JOIN 
        Order o ON fip.DIM_ORDER_POSITION = o.DIM_ORDER_POSITION
    LEFT OUTER JOIN 
        Period p ON fip.Date_dim = p.DIM_DATE
    LEFT OUTER JOIN 
        Supplier status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    LEFT OUTER JOIN 
        Value type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
    LEFT OUTER JOIN 
        Category tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE 
        o.TXT_ORDER_POSITION_LONG = 'UPPER BEARING UCF 215 WITH GUARD TRAIN 3 (POR004.5300009649.00010)' AND
        p.YEAR_OFFSET = 0 AND
        ss.DIM_SUPPLIER_STATUS = 'E' AND
        vt.DIM_VALUE_TYPE = 'I' AND
        ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY 
        o.TXT_ORDER_POSITION_LONG
),
TopOrderSpend AS (
    SELECT 
        TXT_ORDER_POSITION_LONG, 
        TotalSpend
    FROM 
        OrderSpend
    ORDER BY 
        TotalSpend DESC
    OFFSET 0 ROWS FETCH NEXT 5 ROWS ONLY
)
SELECT 
    *
FROM 
    TopOrderSpend;