WITH SupplierSpend AS (
    SELECT 
        s.DIM_SUPPLIER, 
        s.TXT_CONS_SUPPLIER_L1, 
        SUM(f.MES_SPEND_CURR_1) AS GroupedSpend
    FROM 
        Fact_invoice_position f
    JOIN 
        Period p ON f.Date_dim = p.DIM_DATE
    JOIN 
        Supplier s ON f.DIM_SUPPLIER = s.DIM_SUPPLIER
    JOIN 
        Supplier_status ss ON f.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN 
        Value_type vt ON f.dim_value_type = vt.DIM_VALUE_TYPE
    JOIN 
        Category_tree ct ON f.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE 
        p.YEAR_OFFSET = 0 AND
        ss.DIM_SUPPLIER_STATUS = 'E' AND
        vt.DIM_VALUE_TYPE = 'I' AND
        ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY 
        s.DIM_SUPPLIER, s.TXT_CONS_SUPPLIER_L1
),
TotalSpend AS (
    SELECT SUM(GroupedSpend) AS TotalSpend FROM SupplierSpend
),
RunningSpend AS (
    SELECT 
        ss.DIM_SUPPLIER, 
        ss.TXT_CONS_SUPPLIER_L1, 
        ss.GroupedSpend, 
        SUM(ss.GroupedSpend) OVER (ORDER BY ss.GroupedSpend DESC) / ts.TotalSpend AS RunningPercSpend
    FROM 
        SupplierSpend ss, TotalSpend ts
),
Top80SpendSuppliersCount AS (
    SELECT COUNT(*) AS NumberOfSuppliers
    FROM RunningSpend
    WHERE RunningPercSpend < 0.80
)
SELECT NumberOfSuppliers AS Number of suppliers covering 80% of spend
FROM Top80SpendSuppliersCount;