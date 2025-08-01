WITH SupplierCountry AS (
    SELECT 
        txt_low_cost_country
    FROM 
        Supplier country
    WHERE 
        txt_low_cost_country = 'High cost country'
),
Period AS (
    SELECT 
        YEAR_OFFSET
    FROM 
        Period
    WHERE 
        YEAR_OFFSET = 0
),
ValueType AS (
    SELECT 
        DIM_VALUE_TYPE
    FROM 
        Value type
    WHERE 
        DIM_VALUE_TYPE = 'I'
),
SupplierStatus AS (
    SELECT 
        DIM_SUPPLIER_STATUS
    FROM 
        Supplier status
    WHERE 
        DIM_SUPPLIER_STATUS = 'E'
),
ReportingCurrency AS (
    SELECT 
        DIM_REPORTING_CURRENCY
    FROM 
        Reporting currency
    WHERE 
        DIM_REPORTING_CURRENCY = 'CURR_1'
),
CategoryTree AS (
    SELECT 
        TXT_CATEGORY_LEVEL_2
    FROM 
        Category tree
    WHERE 
        TXT_CATEGORY_LEVEL_2 = 'Bearings'
)
SELECT 
    SUM(Fact invoice position.MES_SPEND_CURR_1) AS TotalSpend
FROM 
    Fact invoice position
JOIN 
    Period ON Fact invoice position.Date_dim = Period.DIM_DATE
JOIN 
    Supplier country ON Fact invoice position.DIM_COUNTRY = Supplier country.dim_country
JOIN 
    Supplier status ON Fact invoice position.DIM_SUPPLIER_STATUS = Supplier status.DIM_SUPPLIER_STATUS
JOIN 
    Value type ON Fact invoice position.dim_value_type = Value type.DIM_VALUE_TYPE
JOIN 
    Category tree ON Fact invoice position.DIM_SOURCING_TREE = Category tree.DIM_SOURCING_TREE
WHERE 
    Period.YEAR_OFFSET = 0
    AND Supplier country.txt_low_cost_country = 'High cost country'
    AND Supplier status.DIM_SUPPLIER_STATUS = 'E'
    AND Value type.DIM_VALUE_TYPE = 'I'
    AND Category tree.TXT_CATEGORY_LEVEL_2 = 'Bearings';