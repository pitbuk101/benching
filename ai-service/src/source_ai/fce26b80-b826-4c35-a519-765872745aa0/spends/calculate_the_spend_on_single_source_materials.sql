WITH FactInvoicePosition AS (
    SELECT 
        DIM_MATERIAL, 
        DIM_SUPPLIER, 
        MES_SPEND_CURR_1
    FROM 
        Fact invoice position
),
Material AS (
    SELECT 
        DIM_MATERIAL
    FROM 
        Material
),
JoinedData AS (
    SELECT 
        fip.DIM_MATERIAL, 
        fip.DIM_SUPPLIER, 
        fip.MES_SPEND_CURR_1
    FROM 
        FactInvoicePosition fip
    JOIN 
        Material m ON fip.DIM_MATERIAL = m.DIM_MATERIAL
),
DCountSupplier AS (
    SELECT 
        DIM_MATERIAL, 
        COUNT(DISTINCT DIM_SUPPLIER) AS SupplierCount
    FROM 
        JoinedData
    GROUP BY 
        DIM_MATERIAL
),
SumSpend AS (
    SELECT 
        DIM_MATERIAL, 
        SUM(MES_SPEND_CURR_1) AS TotalSpend
    FROM 
        JoinedData
    GROUP BY 
        DIM_MATERIAL
)
SELECT 
    dcs.DIM_MATERIAL, 
    dcs.SupplierCount, 
    ss.TotalSpend
FROM 
    DCountSupplier dcs
JOIN 
    SumSpend ss ON dcs.DIM_MATERIAL = ss.DIM_MATERIAL;