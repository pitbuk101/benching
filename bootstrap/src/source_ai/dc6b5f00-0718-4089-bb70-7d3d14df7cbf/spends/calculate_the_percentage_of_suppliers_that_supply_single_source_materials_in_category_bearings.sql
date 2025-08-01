WITH Period_Filter AS (
    SELECT DIM_DATE
    FROM Period
    WHERE YEAR_OFFSET = 0
),

Supplier_Status_Filter AS (
    SELECT DIM_SUPPLIER_STATUS
    FROM Supplier status
    WHERE DIM_SUPPLIER_STATUS = 'E'
),

Value_Type_Filter AS (
    SELECT DIM_VALUE_TYPE
    FROM Value type
    WHERE DIM_VALUE_TYPE = 'I'
),

Category_Tree_Filter AS (
    SELECT DIM_SOURCING_TREE
    FROM Category tree
    WHERE TXT_CATEGORY_LEVEL_2 = 'Bearings'
),

Filtered_Fact_Invoice_Position AS (
    SELECT fip.*
    FROM Fact invoice position fip
    JOIN Period_Filter pf ON fip.Date_dim = pf.DIM_DATE
    JOIN Supplier_Status_Filter ssf ON fip.DIM_SUPPLIER_STATUS = ssf.DIM_SUPPLIER_STATUS
    JOIN Value_Type_Filter vtf ON fip.dim_value_type = vtf.DIM_VALUE_TYPE
    JOIN Category_Tree_Filter ctf ON fip.DIM_SOURCING_TREE = ctf.DIM_SOURCING_TREE
),

Material_Count AS (
    SELECT DIM_SUPPLIER, COUNT(DIM_MATERIAL) AS Material_Count
    FROM Filtered_Fact_Invoice_Position
    GROUP BY DIM_SUPPLIER
),

Single_Source_Suppliers AS (
    SELECT DIM_SUPPLIER
    FROM Material_Count
    WHERE Material_Count = 1
),

Suppliers_Count AS (
    SELECT COUNT(DISTINCT DIM_SUPPLIER) AS Suppliers_Count
    FROM Filtered_Fact_Invoice_Position
),

SS_Suppliers_Perct AS (
    SELECT CAST(COUNT(*) AS FLOAT) / (SELECT Suppliers_Count FROM Suppliers_Count) AS SS_Suppliers_Perct
    FROM Single_Source_Suppliers
)

SELECT *
FROM SS_Suppliers_Perct;