WITH ValueType AS (
    SELECT
        DIM_VALUE_TYPE
    FROM
        Value type
),
FactInvoicePosition AS (
    SELECT
        SUM(MES_QUANTITY) AS TotalQuantity
    FROM
        Fact invoice position
)
SELECT
    vt.DIM_VALUE_TYPE,
    fip.TotalQuantity
FROM
    ValueType vt,
    FactInvoicePosition fip;