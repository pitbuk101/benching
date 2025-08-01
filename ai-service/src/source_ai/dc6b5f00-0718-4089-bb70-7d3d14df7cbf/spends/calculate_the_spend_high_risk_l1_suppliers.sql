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
HighRiskSuppliers AS (
    SELECT
        DIM_SUPPLIER
    FROM Supplier
    WHERE
        TXT_SUPPLIER_RISK_BUCKET = 'High'
),
FactInvoicePosition AS (
    SELECT
        DIM_SUPPLIER,
        SUM(MES_SPEND_CURR_1) AS TotalSpend,
        COUNT(*) AS Count
    FROM Fact invoice position

    GROUP BY DIM_SUPPLIER
),
HighRiskSpend AS (
    SELECT
        SUM(Fact invoice position.MES_SPEND_CURR_1) AS TotalSpend
    FROM Fact invoice position
    JOIN Supplier ON Fact invoice position.DIM_SUPPLIER = Supplier.DIM_SUPPLIER
    WHERE
        Supplier.TXT_SUPPLIER_RISK_BUCKET = 'High'
)
SELECT
    HighRiskSpend.TotalSpend
FROM HighRiskSpend;