WITH RegionSpend AS (
    SELECT 
        sc.txt_region AS Region, 
        SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
    FROM 
        Fact invoice position fip
    JOIN 
        Period p ON fip.Date_dim = p.DIM_DATE
    JOIN 
        Supplier country sc ON fip.DIM_COUNTRY = sc.dim_country
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
        sc.txt_region
),
TopRegionSpend AS (
    SELECT 
        Region, 
        TotalSpend
    FROM 
        RegionSpend
    ORDER BY 
        TotalSpend DESC
    OFFSET 0 ROWS FETCH NEXT 5 ROWS ONLY
)
SELECT 
    Region, 
    TotalSpend
FROM 
    TopRegionSpend;