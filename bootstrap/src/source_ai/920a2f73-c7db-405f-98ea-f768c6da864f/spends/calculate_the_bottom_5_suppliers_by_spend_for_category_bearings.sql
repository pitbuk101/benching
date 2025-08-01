WITH SupplierSpend AS (
    SELECT 
        s.TXT_CONS_SUPPLIER_L1, 
        SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
    FROM 
        Fact invoice position fip
    JOIN 
        Period p ON fip.Date_dim = p.DIM_DATE
    JOIN 
        Supplier s ON fip.DIM_SUPPLIER = s.DIM_SUPPLIER
    JOIN 
        Supplier status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN 
        Value type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
    JOIN 
        Category tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE 
        p.YEAR_OFFSET = 0 AND
        ss.DIM_SUPPLIER_STATUS = 'E' AND
        vt.DIM_VALUE_TYPE = 'I' AND
        ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY 
        s.TXT_CONS_SUPPLIER_L1
),
BottomSupplierSpend AS (
    SELECT 
         
        TXT_CONS_SUPPLIER_L1, 
        TotalSpend
    FROM 
        SupplierSpend
    ORDER BY 
        TotalSpend ASC
)
SELECT 
    *
FROM 
    BottomSupplierSpend;