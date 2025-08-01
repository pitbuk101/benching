WITH ValueType AS (
    SELECT
        DIM_VALUE_TYPE
    FROM
        Value type
),
ReportingCurrency AS (
    SELECT
        DIM_REPORTING_CURRENCY
    FROM
        Reporting currency
),
FactInvoicePosition AS (
    SELECT
        SUM(MES_SPEND_CURR_1) AS TotalSpend
    FROM
        Fact invoice position
)
SELECT
    ValueType.DIM_VALUE_TYPE,
    ReportingCurrency.DIM_REPORTING_CURRENCY,
    FactInvoicePosition.TotalSpend
FROM
    ValueType,
    ReportingCurrency,
    FactInvoicePosition;