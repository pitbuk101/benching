WITH PaymentTermSpend AS (
    SELECT
        pt.TXT_CONS_PAYMENT_TERM,
        SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
    FROM
        Fact invoice position fip
    JOIN Period p ON fip.Date_dim = p.DIM_DATE
    JOIN Supplier status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN Value type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
    JOIN Category tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    JOIN Payment term pt ON fip.DIM_PAYMENT_TERM = pt.DIM_PAYMENT_TERM
    WHERE
        p.YEAR_OFFSET = 0
        AND ss.DIM_SUPPLIER_STATUS = 'E'
        AND vt.DIM_VALUE_TYPE = 'I'
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY
        pt.TXT_CONS_PAYMENT_TERM
),
BottomPaymentTermSpend AS (
    SELECT
        TXT_CONS_PAYMENT_TERM,
        TotalSpend
    FROM
        PaymentTermSpend
    ORDER BY
        TotalSpend ASC
    LIMIT 5
)
SELECT
    *
FROM
    BottomPaymentTermSpend;