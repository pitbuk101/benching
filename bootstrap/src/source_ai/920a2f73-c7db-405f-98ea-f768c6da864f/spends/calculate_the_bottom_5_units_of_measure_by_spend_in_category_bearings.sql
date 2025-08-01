WITH UOMSpend AS (
    SELECT 
        uom.TXT_UOM_CONS, 
        SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
    FROM 
        Fact invoice position fip
    LEFT OUTER JOIN 
        Period p ON fip.Date_dim = p.DIM_DATE
    LEFT OUTER JOIN 
        Supplier status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    LEFT OUTER JOIN 
        Unit of measurement uom ON fip.DIM_UOM = uom.DIM_UOM
    LEFT OUTER JOIN 
        Value type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
    LEFT OUTER JOIN 
        Category tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE 
        p.YEAR_OFFSET = 0 AND
        ss.DIM_SUPPLIER_STATUS = 'E' AND
        vt.DIM_VALUE_TYPE = 'I' AND
        ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY 
        uom.TXT_UOM_CONS
),
BottomUOMSpend AS (
    SELECT  
        TXT_UOM_CONS, 
        TotalSpend
    FROM 
        UOMSpend
    ORDER BY 
        TotalSpend ASC
)
SELECT 
    *
FROM 
    BottomUOMSpend;