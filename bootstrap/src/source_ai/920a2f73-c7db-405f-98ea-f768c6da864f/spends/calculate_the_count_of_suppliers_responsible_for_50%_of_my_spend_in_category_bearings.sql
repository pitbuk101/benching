WITH SupplierSpend AS (
    SELECT 
        s.DIM_SUPPLIER, 
        s.TXT_CONS_SUPPLIER_L1, 
        SUM(fip.MES_SPEND_CURR_1) AS GroupedSpend
    FROM 
        Fact invoice position fip
    JOIN 
        Period p ON fip.Date_dim = p.DIM_DATE
    JOIN 
        Supplier s ON fip.DIM_SUPPLIER = s.DIM_SUPPLIER
    JOIN 
        Supplier status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN 
        Value type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
    JOIN 
        Category tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
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
Top50SpendSuppliersCount AS (
    SELECT COUNT(*) AS NumberOfSuppliers
    FROM RunningSpend
    WHERE RunningPercSpend < 0.50
)
SELECT NumberOfSuppliers AS "Number_of_suppliers_covering_50%_of_spend"
FROM Top50SpendSuppliersCount;