WITH UOMSpend AS (
    SELECT 
        uom.TXT_UOM_CONS, 
        SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
    FROM 
        Fact invoice position fip
    JOIN 
        Period p ON fip.Date_dim = p.DIM_DATE
    JOIN 
        Supplier status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN 
        Unit of measurement uom ON fip.DIM_UOM = uom.DIM_UOM
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
        uom.TXT_UOM_CONS
),
TopUOMSpend AS (
    SELECT 
        TXT_UOM_CONS, 
        TotalSpend
    FROM 
        UOMSpend
    ORDER BY 
        TotalSpend DESC
    LIMIT 5
)
SELECT 
    *
FROM 
    TopUOMSpend;