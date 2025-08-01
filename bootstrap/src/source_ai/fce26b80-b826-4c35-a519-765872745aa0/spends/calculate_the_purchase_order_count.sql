WITH ValueType AS (
    SELECT
        DIM_VALUE_TYPE
    FROM Value type
),
OrderData AS (
    SELECT
        KEY_ORDER
    FROM Order
),
ReportingCurrency AS (
    SELECT
        DIM_REPORTING_CURRENCY
    FROM Reporting currency
),
FactInvoicePosition AS (
    SELECT
        Order.KEY_ORDER,
        SUM(Fact invoice position.MES_SPEND_CURR_1) AS TotalSpend
    FROM Fact invoice position
    LEFT OUTER JOIN Order
        ON Fact invoice position.DIM_ORDER_POSITION = Order.DIM_ORDER_POSITION
    GROUP BY Order.KEY_ORDER
),
FilteredOrder AS (
    SELECT
        KEY_ORDER
    FROM Order

),
DistinctOrderCount AS (
    SELECT
        COUNT(DISTINCT KEY_ORDER) AS OrderCount
    FROM Order
    WHERE
        KEY_ORDER <> '-1'
)
SELECT
    OrderCount
FROM DistinctOrderCount;