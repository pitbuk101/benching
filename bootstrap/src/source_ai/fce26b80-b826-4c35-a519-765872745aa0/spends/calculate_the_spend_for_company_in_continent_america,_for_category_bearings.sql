WITH CompanyFiltered AS (
    SELECT *
    FROM Company
    WHERE txt_continent = 'America'
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
CategoryTreeFiltered AS (
    SELECT *
    FROM CategoryTree
    WHERE TXT_CATEGORY_LEVEL_2 = 'Bearings'
),
ReportingCurrencyFiltered AS (
    SELECT *
    FROM ReportingCurrency
    WHERE DIM_REPORTING_CURRENCY = 'CURR_1'
),
FactInvoicePositionFiltered AS (
    SELECT *
    FROM FactInvoicePosition
    WHERE DIM_COMPANY IN (SELECT DIM_COMPANY FROM CompanyFiltered)
      AND Date_dim IN (SELECT DIM_DATE FROM PeriodFiltered)
      AND DIM_SUPPLIER_STATUS IN (SELECT DIM_SUPPLIER_STATUS FROM SupplierStatusFiltered)
      AND dim_value_type IN (SELECT DIM_VALUE_TYPE FROM ValueTypeFiltered)
      AND DIM_SOURCING_TREE IN (SELECT DIM_SOURCING_TREE FROM CategoryTreeFiltered)
),
SpendCalculation AS (
    SELECT SUM(MES_SPEND_CURR_1) AS TotalSpend
    FROM FactInvoicePositionFiltered
)
SELECT TotalSpend
FROM SpendCalculation;