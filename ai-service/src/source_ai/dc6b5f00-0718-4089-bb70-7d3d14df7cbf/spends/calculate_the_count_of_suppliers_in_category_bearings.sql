WITH FilteredData AS (
    SELECT
        Period.TXT_YEAR,
        Fact invoice position.DIM_SUPPLIER
    FROM Fact invoice position
    LEFT OUTER JOIN Period ON Fact invoice position.Date_dim = Period.DIM_DATE
    LEFT OUTER JOIN Supplier status ON Fact invoice position.DIM_SUPPLIER_STATUS = Supplier status.DIM_SUPPLIER_STATUS
    LEFT OUTER JOIN Value type ON Fact invoice position.dim_value_type = Value type.DIM_VALUE_TYPE
    LEFT OUTER JOIN Category tree ON Fact invoice position.DIM_SOURCING_TREE = Category tree.DIM_SOURCING_TREE
    WHERE
        Period.YEAR_OFFSET = 0 AND
        Supplier status.DIM_SUPPLIER_STATUS = 'E' AND
        Value type.DIM_VALUE_TYPE = 'I' AND
        Category tree.TXT_CATEGORY_LEVEL_2 = 'Bearings'
),
RegionSpend AS (
    SELECT
        TXT_YEAR,
        COUNT(DIM_SUPPLIER) AS Suppliers count
    FROM FilteredData
    GROUP BY TXT_YEAR
)
SELECT
    TXT_YEAR,
    Suppliers count
FROM RegionSpend;