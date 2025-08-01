WITH TotalSuppliers AS (
    SELECT COUNT(DISTINCT Fact invoice position.DIM_SUPPLIER) AS SuppliersCount
    FROM Fact invoice position
    JOIN Period ON Fact invoice position.Date_dim = Period.DIM_DATE
    JOIN Value type ON Fact invoice position.dim_value_type = Value type.DIM_VALUE_TYPE
    JOIN Supplier status ON Fact invoice position.DIM_SUPPLIER_STATUS = Supplier status.DIM_SUPPLIER_STATUS
    JOIN Category tree ON Fact invoice position.DIM_SOURCING_TREE = Category tree.DIM_SOURCING_TREE
    WHERE Period.YEAR_OFFSET = 0
      AND Value type.DIM_VALUE_TYPE = 'I'
      AND Supplier status.DIM_SUPPLIER_STATUS = 'E'
      AND Category tree.TXT_CATEGORY_LEVEL_2 = 'Bearings'
),
LowCostCountrySuppliers AS (
    SELECT COUNT(DISTINCT Fact invoice position.DIM_SUPPLIER) AS SuppliersCount
    FROM Fact invoice position
    JOIN Period ON Fact invoice position.Date_dim = Period.DIM_DATE
    JOIN Supplier country ON Fact invoice position.DIM_COUNTRY = Supplier country.dim_country
    JOIN Value type ON Fact invoice position.dim_value_type = Value type.DIM_VALUE_TYPE
    JOIN Supplier status ON Fact invoice position.DIM_SUPPLIER_STATUS = Supplier status.DIM_SUPPLIER_STATUS
    JOIN Category tree ON Fact invoice position.DIM_SOURCING_TREE = Category tree.DIM_SOURCING_TREE
    WHERE Period.YEAR_OFFSET = 0
      AND Supplier country.txt_low_cost_country = 'Low cost country'
      AND Value type.DIM_VALUE_TYPE = 'I'
      AND Supplier status.DIM_SUPPLIER_STATUS = 'E'
      AND Category tree.TXT_CATEGORY_LEVEL_2 = 'Bearings'
)
SELECT 
    LowCostCountrySuppliers.SuppliersCount AS Count of suppliers from low cost countries,
    TotalSuppliers.SuppliersCount AS Total suppliers count,
    (LowCostCountrySuppliers.SuppliersCount * 100.0 / TotalSuppliers.SuppliersCount) AS Percentage of suppliers from low cost countries
FROM TotalSuppliers, LowCostCountrySuppliers;