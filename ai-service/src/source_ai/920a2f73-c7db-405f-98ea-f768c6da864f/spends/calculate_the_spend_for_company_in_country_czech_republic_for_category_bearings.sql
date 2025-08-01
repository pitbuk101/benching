WITH CompanyFiltered AS (
    SELECT *
    FROM Company
    WHERE TXT_COUNTRY = 'Czech Republic'
),
PeriodFiltered AS (
    SELECT *
    FROM Period
    WHERE YEAR_OFFSET = 0
),
ValueTypeFiltered AS (
    SELECT *
    FROM ValueType
    WHERE DIM_VALUE_TYPE = 'I'
),
SupplierStatusFiltered AS (
    SELECT *
    FROM SupplierStatus
    WHERE DIM_SUPPLIER_STATUS = 'E'
),
ReportingCurrencyFiltered AS (
    SELECT *
    FROM ReportingCurrency
    WHERE DIM_REPORTING_CURRENCY = 'CURR_1'
),
CategoryTreeFiltered AS (
    SELECT *
    FROM CategoryTree
    WHERE TXT_CATEGORY_LEVEL_2 = 'Bearings'
)
SELECT
    SUM(FIP.MES_SPEND_CURR_1) AS TotalSpend
FROM
    FactInvoicePosition FIP
    JOIN CompanyFiltered C ON FIP.DIM_COMPANY = C.DIM_COMPANY
    JOIN PeriodFiltered P ON FIP.Date_dim = P.DIM_DATE
    JOIN SupplierStatusFiltered SS ON FIP.DIM_SUPPLIER_STATUS = SS.DIM_SUPPLIER_STATUS
    JOIN ValueTypeFiltered VT ON FIP.dim_value_type = VT.DIM_VALUE_TYPE
    JOIN CategoryTreeFiltered CT ON FIP.DIM_SOURCING_TREE = CT.DIM_SOURCING_TREE
;