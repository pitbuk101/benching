WITH MaterialFilter AS (
    SELECT
        DIM_MATERIAL
    FROM
        Material
    
),
FilteredInvoicePosition AS (
    SELECT
        Fact invoice position.DIM_MATERIAL
    FROM
        Fact invoice position
    LEFT OUTER JOIN
        MaterialFilter
    ON
        Fact invoice position.DIM_MATERIAL = MaterialFilter.DIM_MATERIAL
    WHERE
        MaterialFilter.DIM_MATERIAL IS NOT NULL
),
MaterialCount AS (
    SELECT
        COUNT(DISTINCT DIM_MATERIAL) AS MaterialCount
    FROM
        FilteredInvoicePosition
)
SELECT
    MaterialCount
FROM
    MaterialCount;