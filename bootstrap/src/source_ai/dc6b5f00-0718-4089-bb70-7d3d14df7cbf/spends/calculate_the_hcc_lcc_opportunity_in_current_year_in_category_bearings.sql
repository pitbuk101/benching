WITH ValueType AS (
    SELECT
        DIM_VALUE_TYPE
    FROM Value type
),
ReportingCurrency AS (
    SELECT
        DIM_REPORTING_CURRENCY
    FROM Reporting currency
),
FactInvoicePosition AS (
    SELECT
        SUM(MES_SPEND_CURR_1) AS TotalSpend,
        COUNT(*) AS TotalCount
    FROM Fact invoice position
    LEFT OUTER JOIN Supplier country ON Fact invoice position.DIM_COUNTRY = Supplier country.dim_country
    WHERE Supplier country.txt_low_cost_country = 'Low cost country'
)
SELECT
    TotalSpend,
    TotalCount
FROM FactInvoicePosition;