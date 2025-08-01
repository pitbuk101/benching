WITH CategoryTreeFiltered AS (
    SELECT 
        TXT_CATEGORY_LEVEL_2, 
        DIM_SOURCING_TREE
    FROM 
        Category tree
    WHERE 
        TXT_CATEGORY_LEVEL_2 = 'Bearings' AND 
        TXT_CATEGORY_LEVEL_2 = 'Hardware'
),

PeriodFiltered AS (
    SELECT 
        DIM_DATE
    FROM 
        Period
    WHERE 
        YEAR_OFFSET = 0
),

ValueTypeFiltered AS (
    SELECT 
        DIM_VALUE_TYPE
    FROM 
        Value type
    WHERE 
        DIM_VALUE_TYPE = 'I'
),

SupplierStatusFiltered AS (
    SELECT 
        DIM_SUPPLIER_STATUS
    FROM 
        Supplier status
    WHERE 
        DIM_SUPPLIER_STATUS = 'E'
),

ReportingCurrencyFiltered AS (
    SELECT 
        DIM_REPORTING_CURRENCY
    FROM 
        Reporting currency
    WHERE 
        DIM_REPORTING_CURRENCY = 'CURR_1'
),

FactInvoicePositionFiltered AS (
    SELECT 
        MES_SPEND_CURR_1, 
        Date_dim, 
        DIM_SUPPLIER_STATUS, 
        dim_value_type, 
        DIM_SOURCING_TREE
    FROM 
        Fact invoice position
)

SELECT 
    SUM(FIP.MES_SPEND_CURR_1) AS TotalSpend
FROM 
    FactInvoicePositionFiltered FIP
    JOIN PeriodFiltered P ON FIP.Date_dim = P.DIM_DATE
    JOIN SupplierStatusFiltered SS ON FIP.DIM_SUPPLIER_STATUS = SS.DIM_SUPPLIER_STATUS
    JOIN ValueTypeFiltered VT ON FIP.dim_value_type = VT.DIM_VALUE_TYPE
    JOIN CategoryTreeFiltered CT ON FIP.DIM_SOURCING_TREE = CT.DIM_SOURCING_TREE
    JOIN ReportingCurrencyFiltered RC ON 1=1
