WITH FilteredPeriod AS (
    SELECT TXT_YEAR
    FROM Period
    WHERE YEAR_OFFSET = 0
),
FilteredValueType AS (
    SELECT DIM_VALUE_TYPE
    FROM Value type
    WHERE DIM_VALUE_TYPE = 'I'
),
FilteredSupplierStatus AS (
    SELECT DIM_SUPPLIER_STATUS
    FROM Supplier status
    WHERE DIM_SUPPLIER_STATUS = 'E'
),
FilteredReportingCurrency AS (
    SELECT DIM_REPORTING_CURRENCY
    FROM Reporting currency
    WHERE DIM_REPORTING_CURRENCY = 'CURR_1'
),
FilteredCategoryTree AS (
    SELECT TXT_CATEGORY_LEVEL_2
    FROM Category tree
    WHERE TXT_CATEGORY_LEVEL_2 = 'Bearings'
),
FilteredFactInvoicePosition AS (
    SELECT Date_dim, DIM_SUPPLIER_STATUS, dim_value_type, DIM_SOURCING_TREE, MES_SPEND_CURR_1
    FROM Fact invoice position
)
SELECT 
    p.TXT_YEAR,
    SUM(f.MES_SPEND_CURR_1) AS TotalSpend
FROM 
    FilteredFactInvoicePosition f
    JOIN FilteredPeriod p ON f.Date_dim = p.DIM_DATE
    JOIN FilteredSupplierStatus s ON f.DIM_SUPPLIER_STATUS = s.DIM_SUPPLIER_STATUS
    JOIN FilteredValueType v ON f.dim_value_type = v.DIM_VALUE_TYPE
    JOIN FilteredCategoryTree c ON f.DIM_SOURCING_TREE = c.DIM_SOURCING_TREE
WHERE 
    p.YEAR_OFFSET = 0
    AND s.DIM_SUPPLIER_STATUS = 'E'
    AND v.DIM_VALUE_TYPE = 'I'
    AND c.TXT_CATEGORY_LEVEL_2 = 'Bearings'
GROUP BY 
    p.TXT_YEAR;