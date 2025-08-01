WITH OrderRefSpend AS (
    SELECT
        Order reference.TXT_ORDER_REFERENCE,
        SUM(Fact invoice position.MES_SPEND_CURR_1) AS TotalSpend
    FROM
        Fact invoice position
    LEFT OUTER JOIN Order reference ON Fact invoice position.DIM_ORDER_REFERENCE = Order reference.DIM_ORDER_REFERENCE
    LEFT OUTER JOIN Period ON Fact invoice position.Date_dim = Period.DIM_DATE
    LEFT OUTER JOIN Supplier status ON Fact invoice position.DIM_SUPPLIER_STATUS = Supplier status.DIM_SUPPLIER_STATUS
    LEFT OUTER JOIN Value type ON Fact invoice position.dim_value_type = Value type.DIM_VALUE_TYPE
    LEFT OUTER JOIN Category tree ON Fact invoice position.DIM_SOURCING_TREE = Category tree.DIM_SOURCING_TREE
    LEFT OUTER JOIN Reporting Currency ON Fact invoice position.DIM_REPORTING_CURRENCY = Reporting Currency.DIM_REPORTING_CURRENCY
    WHERE
        Period.YEAR_OFFSET = 0 AND
        Supplier status.DIM_SUPPLIER_STATUS = 'E' AND
        Value type.DIM_VALUE_TYPE = 'I' AND
        Category tree.TXT_CATEGORY_LEVEL_2 = 'Bearings' AND
        Reporting Currency.DIM_REPORTING_CURRENCY = 'CURR_1'
    GROUP BY
        Order reference.TXT_ORDER_REFERENCE
)
SELECT * FROM OrderRefSpend;