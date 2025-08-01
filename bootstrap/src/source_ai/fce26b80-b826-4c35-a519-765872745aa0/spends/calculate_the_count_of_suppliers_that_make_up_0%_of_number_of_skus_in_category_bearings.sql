WITH SupplierSKUCount AS (
    SELECT 
        s.DIM_SUPPLIER, 
        s.TXT_SUPPLIER, 
        COUNT(m.DIM_MATERIAL) AS GroupedSKUCount
    FROM 
        Fact invoice position f
    JOIN 
        Period p ON f.Date_dim = p.DIM_DATE
    JOIN 
        Supplier s ON f.DIM_SUPPLIER = s.DIM_SUPPLIER
    JOIN 
        Supplier status ss ON f.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN 
        Value type vt ON f.dim_value_type = vt.DIM_VALUE_TYPE
    JOIN 
        Material m ON f.DIM_MATERIAL = m.DIM_MATERIAL
    JOIN 
        Category tree ct ON f.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE 
        p.YEAR_OFFSET = 0 
        AND ss.DIM_SUPPLIER_STATUS = 'E' 
        AND vt.DIM_VALUE_TYPE = 'I' 
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY 
        s.DIM_SUPPLIER, s.TXT_SUPPLIER
), 
TotalSKUCount AS (
    SELECT SUM(GroupedSKUCount) AS TotalSKUCount
    FROM SupplierSKUCount
), 
RunningSKUCount AS (
    SELECT 
        s.DIM_SUPPLIER, 
        s.TXT_SUPPLIER, 
        s.GroupedSKUCount, 
        SUM(s.GroupedSKUCount) OVER (ORDER BY s.GroupedSKUCount DESC) / t.TotalSKUCount AS RunningPercSKUCount
    FROM 
        SupplierSKUCount s, 
        TotalSKUCount t
), 
Top50SKUCountSuppliers AS (
    SELECT COUNT(*) AS NumberOfSuppliers
    FROM RunningSKUCount
    WHERE RunningPercSKUCount < 0.50
)
SELECT * FROM Top50SKUCountSuppliers;