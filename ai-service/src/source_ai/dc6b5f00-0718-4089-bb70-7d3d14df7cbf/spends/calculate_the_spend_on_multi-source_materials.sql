WITH MaterialData AS (
    SELECT
        Material .DIM MATERIAL  AS Material
    FROM Fact invoice position 
    LEFT OUTER JOIN Material  ON Fact invoice position .DIM MATERIAL  = Material .DIM MATERIAL 
),
SupplierCount AS (
    SELECT
        Material .DIM MATERIAL  AS Material,
        DCOUNT(Fact invoice position .DIM SUPPLIER ) AS SupplierCount
    FROM Fact invoice position 
    LEFT OUTER JOIN Material  ON Fact invoice position .DIM MATERIAL  = Material .DIM MATERIAL 
    GROUP BY Material .DIM MATERIAL 
),
ValueTypeData AS (
    SELECT
        Value type .DIM VALUE TYPE  AS ValueType
    FROM Value type 
),
ReportingCurrencyData AS (
    SELECT
        Reporting currency .DIM REPORTING CURRENCY  AS ReportingCurrency
    FROM Reporting currency 
),
SpendData AS (
    SELECT
        Material .DIM MATERIAL  AS Material,
        SUM(Fact invoice position .MES SPEND CURR 1 ) AS TotalSpend
    FROM Fact invoice position 
    LEFT OUTER JOIN Material  ON Fact invoice position .DIM MATERIAL  = Material .DIM MATERIAL 
    GROUP BY Material .DIM MATERIAL 
)
SELECT
    MaterialData.Material,
    SupplierCount.SupplierCount,
    SpendData.TotalSpend
FROM MaterialData
JOIN SupplierCount ON MaterialData.Material = SupplierCount.Material
JOIN SpendData ON MaterialData.Material = SpendData.Material;