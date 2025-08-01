WITH SupplierContinentSpend AS (
    SELECT 
        sc.txt_continent AS SupplierContinent, 
        SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
    FROM 
        Fact_invoice_position fip
    JOIN 
        Period p ON fip.Date_dim = p.DIM_DATE
    JOIN 
        Supplier_country sc ON fip.DIM_COUNTRY = sc.dim_country
    JOIN 
        Supplier_status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN 
        Value_type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
    JOIN 
        Category_tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE 
        p.YEAR_OFFSET = 0 AND
        ss.DIM_SUPPLIER_STATUS = 'E' AND
        vt.DIM_VALUE_TYPE = 'I' AND
        ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY 
        sc.txt_continent
), 
TopSupplierContinentSpend AS (
    SELECT 
        SupplierContinent, 
        TotalSpend
    FROM 
        SupplierContinentSpend
    ORDER BY 
        TotalSpend DESC
    LIMIT 5
)
SELECT 
    *
FROM 
    TopSupplierContinentSpend;