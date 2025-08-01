WITH FilteredPeriod AS (
    SELECT TXT_YEAR
    FROM Period
    WHERE YEAR_OFFSET = 0
),
FilteredValueType AS (
    SELECT DIM_VALUE_TYPE
    FROM Value type
    WHERE DIM_VALUE_TYPE = 'I'
),
FilteredSupplierStatus AS (
    SELECT DIM_SUPPLIER_STATUS
    FROM Supplier status
    WHERE DIM_SUPPLIER_STATUS = 'E'
),
FilteredCategoryTree AS (
    SELECT TXT_CATEGORY_LEVEL_2
    FROM Category tree
    WHERE TXT_CATEGORY_LEVEL_2 = 'Bearings'
),
SupplierCount AS (
    SELECT
        p.TXT_YEAR,
        COUNT(s.DIM_SUPPLIER) AS Supplier_Count
    FROM
        Fact invoice position fip
        JOIN FilteredPeriod p ON fip.Date_dim = p.DIM_DATE
        JOIN FilteredValueType vt ON fip.DIM_VALUE_TYPE = vt.DIM_VALUE_TYPE
        JOIN FilteredSupplierStatus ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
        JOIN FilteredCategoryTree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    GROUP BY
        p.TXT_YEAR
)
SELECT *
FROM SupplierCount;