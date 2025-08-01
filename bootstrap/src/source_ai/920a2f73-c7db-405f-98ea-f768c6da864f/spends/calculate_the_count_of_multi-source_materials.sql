WITH MaterialData AS (
    SELECT
        Material .DIM MATERIAL  AS Material $DIM MATERIAL ,
        Fact invoice position .DIM SUPPLIER 
    FROM Fact invoice position 
    LEFT OUTER JOIN Material  ON Fact invoice position .DIM MATERIAL  = Material .DIM MATERIAL 
),

MaterialCount AS (
    SELECT
        Material .DIM MATERIAL  AS Material $DIM MATERIAL ,
        COUNT(*) AS MaterialCount
    FROM Fact invoice position 
    LEFT OUTER JOIN Material  ON Fact invoice position .DIM MATERIAL  = Material .DIM MATERIAL 
    GROUP BY Material .DIM MATERIAL 
),

DistinctSupplierCount AS (
    SELECT
        Material .DIM MATERIAL  AS Material $DIM MATERIAL ,
        COUNT(DISTINCT Fact invoice position .DIM SUPPLIER ) AS DistinctSupplierCount
    FROM Fact invoice position 
    LEFT OUTER JOIN Material  ON Fact invoice position .DIM MATERIAL  = Material .DIM MATERIAL 
    GROUP BY Material .DIM MATERIAL 
)

SELECT
    m.Material $DIM MATERIAL ,
    mc.MaterialCount,
    dsc.DistinctSupplierCount
FROM MaterialData m
JOIN MaterialCount mc ON m.Material $DIM MATERIAL  = mc.Material $DIM MATERIAL 
JOIN DistinctSupplierCount dsc ON m.Material $DIM MATERIAL  = dsc.Material $DIM MATERIAL ;