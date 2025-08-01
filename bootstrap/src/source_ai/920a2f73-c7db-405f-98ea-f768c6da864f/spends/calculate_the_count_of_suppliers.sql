WITH FactInvoicePosition AS (
    SELECT 
        DIM_SUPPLIER
    FROM 
        FactInvoicePosition
),
SupplierCount AS (
    SELECT 
        COUNT(DISTINCT DIM_SUPPLIER) AS SupplierCount
    FROM 
        FactInvoicePosition
)
SELECT 
    SupplierCount
FROM 
    SupplierCount;