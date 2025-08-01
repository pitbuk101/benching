WITH ActiveSuppliers AS (
    SELECT
        Fact invoice position.DIM_SUPPLIER,
        COUNT(*) AS Active Vendors
    FROM
        Fact invoice position
    JOIN
        Period ON Fact invoice position.Date_dim = Period.DIM_DATE
    JOIN
        Supplier status ON Fact invoice position.DIM_SUPPLIER_STATUS = Supplier status.DIM_SUPPLIER_STATUS
    JOIN
        Value type ON Fact invoice position.dim_value_type = Value type.DIM_VALUE_TYPE
    JOIN
        Category tree ON Fact invoice position.DIM_SOURCING_TREE = Category tree.DIM_SOURCING_TREE
    WHERE
        Period.YEAR_OFFSET = 0
        AND Value type.DIM_VALUE_TYPE = 'I'
        AND Supplier status.DIM_SUPPLIER_STATUS = 'E'
        AND Category tree.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY
        Fact invoice position.DIM_SUPPLIER
)
SELECT * FROM ActiveSuppliers;