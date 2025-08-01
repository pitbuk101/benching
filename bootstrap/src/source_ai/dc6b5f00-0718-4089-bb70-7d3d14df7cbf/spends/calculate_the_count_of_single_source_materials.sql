WITH MaterialData AS (
    SELECT
        DIM_MATERIAL AS Material
    FROM Material
),

FactInvoicePositionData AS (
    SELECT
        DIM_MATERIAL,
        DIM_SUPPLIER
    FROM Fact invoice position
),

JoinedData AS (
    SELECT
        m.Material,
        f.DIM_SUPPLIER
    FROM FactInvoicePositionData f
    JOIN MaterialData m ON f.DIM_MATERIAL = m.Material
),

DistinctSupplierCount AS (
    SELECT
        Material,
        COUNT(DISTINCT DIM_SUPPLIER) AS SupplierCount
    FROM JoinedData
    GROUP BY Material
)

SELECT
    Material,
    SupplierCount
FROM DistinctSupplierCount;