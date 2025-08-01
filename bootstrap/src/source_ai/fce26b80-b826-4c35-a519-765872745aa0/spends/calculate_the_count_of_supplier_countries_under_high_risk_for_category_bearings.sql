WITH FilteredData AS (
    SELECT 
        p.TXT_YEAR, 
        fip.DIM_COUNTRY
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
        sc.TXT_COUNTRY_RISK_BUCKET = 'High' AND
        ss.DIM_SUPPLIER_STATUS = 'E' AND
        vt.DIM_VALUE_TYPE = 'I' AND
        ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
),
Supplier_Country_count AS (
    SELECT 
        p.TXT_YEAR, 
        COUNT(DISTINCT fip.DIM_COUNTRY) AS Supplier_Country_count
    FROM 
        FilteredData fd
    GROUP BY 
        fd.TXT_YEAR
)
SELECT 
    *
FROM 
    Supplier_Country_count;