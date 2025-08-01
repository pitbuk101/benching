WITH SupplierHighRisk AS ( 
    SELECT 
        DIM_SUPPLIER, 
        TXT_SUPPLIER_RISK_BUCKET 
    FROM data.VT_C_DIM_Supplier 
    WHERE TXT_SUPPLIER_RISK_BUCKET = 'High' 
), 
FactInvoicePositionFiltered AS ( 
    SELECT 
        f.DIM_MATERIAL, 
        f.DIM_SUPPLIER 
    FROM data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED f 
    JOIN SupplierHighRisk s ON f.DIM_SUPPLIER = s.DIM_SUPPLIER 
    WHERE s.TXT_SUPPLIER_RISK_BUCKET = 'High' 
), 
MaterialFiltered AS ( 
    SELECT 
        f.DIM_MATERIAL 
    FROM FactInvoicePositionFiltered f 
    JOIN data.VT_C_DIM_Material m ON f.DIM_MATERIAL = m.DIM_MATERIAL 
    WHERE m.DIM_MATERIAL IS NOT NULL AND m.DIM_MATERIAL != '-1' 
) 
SELECT 
    COUNT(DISTINCT DIM_MATERIAL) AS HighRiskMaterialCount 
FROM MaterialFiltered;