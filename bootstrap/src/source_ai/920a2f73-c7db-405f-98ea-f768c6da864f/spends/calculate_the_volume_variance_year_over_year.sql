WITH ValueType AS (
    SELECT
        DIM_VALUE_TYPE
    FROM Value type
),

FactInvoicePosition AS (
    SELECT
        SUM(MES_QUANTITY) AS TotalQuantity,
        COUNT(*) AS CountQuantity
    FROM Fact invoice position
),

PeriodData AS (
    SELECT
        DIM_DATE,
        COUNT(*) AS CountDate
    FROM Period
)

SELECT
    vt.DIM_VALUE_TYPE,
    fip.TotalQuantity,
    fip.CountQuantity,
    pd.DIM_DATE,
    pd.CountDate
FROM
    ValueType vt
    CROSS JOIN FactInvoicePosition fip
    CROSS JOIN PeriodData pd;