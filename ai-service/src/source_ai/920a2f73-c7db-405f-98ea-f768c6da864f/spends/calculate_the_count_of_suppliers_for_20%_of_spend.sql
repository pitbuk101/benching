WITH FactInvoicePosition AS (
    SELECT 
        DIM_SUPPLIER, 
        MES_SPEND_CURR_1
    FROM 
        Fact invoice position
),

SupplierSpend AS (
    SELECT 
        DIM_SUPPLIER, 
        SUM(MES_SPEND_CURR_1) AS TotalSpend
    FROM 
        FactInvoicePosition
    GROUP BY 
        DIM_SUPPLIER
),

Top20PercentSuppliers AS (
    SELECT 
        DIM_SUPPLIER, 
        TotalSpend,
        PERCENT_RANK() OVER (ORDER BY TotalSpend DESC) AS PercentRank
    FROM 
        SupplierSpend
),

FilteredSuppliers AS (
    SELECT 
        DIM_SUPPLIER
    FROM 
        Top20PercentSuppliers
    WHERE 
        PercentRank <= 0.20
)

SELECT 
    COUNT(DISTINCT DIM_SUPPLIER) AS Suppliers count for 20prct of spend
FROM 
    FilteredSuppliers;