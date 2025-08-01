WITH SupplierData AS ( 
    SELECT 
        Supplier.DIM_SUPPLIER, 
        Supplier.TXT_SUPPLIER_RISK_BUCKET 
    FROM 
        data.VT_C_DIM_Supplier AS Supplier 
    WHERE 
        Supplier.TXT_SUPPLIER_RISK_BUCKET = 'High' 
), 
FactInvoicePositionData AS ( 
    SELECT 
        FactInvoicePosition.DIM_SUPPLIER 
    FROM 
        data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED AS FactInvoicePosition 
) 
SELECT 
    COUNT(DISTINCT SupplierData.DIM_SUPPLIER) AS HighRiskSupplierCount 
FROM 
    SupplierData 
JOIN 
    FactInvoicePositionData ON SupplierData.DIM_SUPPLIER = FactInvoicePositionData.DIM_SUPPLIER;