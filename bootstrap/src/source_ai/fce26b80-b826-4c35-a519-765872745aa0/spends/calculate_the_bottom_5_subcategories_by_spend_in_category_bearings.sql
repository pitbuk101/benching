WITH SubcategorySpend AS (
    SELECT
        ct.TXT_CATEGORY_LEVEL_2,
        SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
    FROM
        Fact_invoice_position fip
        JOIN Period p ON fip.Date_dim = p.DIM_DATE
        JOIN Supplier_status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
        JOIN Value_type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
        JOIN Category_tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE
        p.YEAR_OFFSET = 0
        AND ss.DIM_SUPPLIER_STATUS = 'E'
        AND vt.DIM_VALUE_TYPE = 'I'
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY
        ct.TXT_CATEGORY_LEVEL_2
),
BottomSubcategorySpend AS (
    SELECT
        
        TXT_CATEGORY_LEVEL_2,
        TotalSpend
    FROM
        SubcategorySpend
    ORDER BY
        TotalSpend ASC
)
SELECT
    *
FROM
    BottomSubcategorySpend;