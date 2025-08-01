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
        SUM(MES_SPEND_CURR_1) AS TotalSpend
    FROM Fact invoice position
),
PeriodData AS (
    SELECT
        DIM_DATE
    FROM Period
),
FilteredFactInvoicePosition AS (
    SELECT
        SUM(Fact invoice position.MES_SPEND_CURR_1) AS TotalSpend,
        COUNT(*) AS Count
    FROM Fact invoice position
    LEFT OUTER JOIN Period ON Fact invoice position.Date_dim = Period.DIM_DATE
    WHERE Period.DIM_DATE IN (44905.000000, 44946.000000, 44987.000000, 45028.000000, 45069.000000, 45110.000000, 45151.000000, 44577.000000, 44618.000000, 44659.000000)
)
SELECT
    ValueType.DIM_VALUE_TYPE,
    ReportingCurrency.DIM_REPORTING_CURRENCY,
    FactInvoicePosition.TotalSpend,
    PeriodData.DIM_DATE,
    FilteredFactInvoicePosition.TotalSpend AS FilteredTotalSpend,
    FilteredFactInvoicePosition.Count AS FilteredCount
FROM ValueType
CROSS JOIN ReportingCurrency
CROSS JOIN FactInvoicePosition
CROSS JOIN PeriodData
CROSS JOIN FilteredFactInvoicePosition;