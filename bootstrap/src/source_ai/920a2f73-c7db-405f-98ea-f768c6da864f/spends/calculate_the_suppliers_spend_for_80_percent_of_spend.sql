WITH ValueType AS (
    SELECT
        DIM_VALUE_TYPE
    FROM
        Value type
),
Supplier AS (
    SELECT
        DIM_SUPPLIER
    FROM
        Supplier
),
ReportingCurrency AS (
    SELECT
        DIM_REPORTING_CURRENCY
    FROM
        Reporting currency
),
SupplierSpend AS (
    SELECT
        Supplier.DIM_SUPPLIER,
        SUM(Fact invoice position.MES_SPEND_CURR_1) AS TotalSpend
    FROM
        Fact invoice position
    LEFT OUTER JOIN
        Supplier ON Fact invoice position.DIM_SUPPLIER = Supplier.DIM_SUPPLIER
    WHERE
        Supplier.DIM_SUPPLIER IS NOT NULL
    GROUP BY
        Supplier.DIM_SUPPLIER
)
SELECT
    SupplierSpend.DIM_SUPPLIER,
    SupplierSpend.TotalSpend
FROM
    SupplierSpend
ORDER BY
    SupplierSpend.TotalSpend DESC
LIMIT 80 PERCENT;