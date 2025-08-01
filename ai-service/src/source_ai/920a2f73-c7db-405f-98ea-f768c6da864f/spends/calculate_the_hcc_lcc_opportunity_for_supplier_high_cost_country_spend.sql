WITH ValueType AS (
    SELECT
        Value type .DIM VALUE TYPE  AS DIM_VALUE_TYPE
    FROM Value type 
),
ReportingCurrency AS (
    SELECT
        Reporting currency .DIM REPORTING CURRENCY  AS DIM_REPORTING_CURRENCY
    FROM Reporting currency 
),
FactInvoicePosition AS (
    SELECT
        SUM(Fact invoice position .MES SPEND CURR 1 ) AS TotalSpend,
        COUNT(*) AS Count
    FROM Fact invoice position 
    LEFT OUTER JOIN Supplier country 
        ON Fact invoice position .DIM COUNTRY  = Supplier country .dim country 
    WHERE
        Supplier country .txt low cost country  = 'High cost country'
)
SELECT
    ValueType.DIM_VALUE_TYPE,
    ReportingCurrency.DIM_REPORTING_CURRENCY,
    FactInvoicePosition.TotalSpend,
    FactInvoicePosition.Count
FROM ValueType
CROSS JOIN ReportingCurrency
CROSS JOIN FactInvoicePosition;