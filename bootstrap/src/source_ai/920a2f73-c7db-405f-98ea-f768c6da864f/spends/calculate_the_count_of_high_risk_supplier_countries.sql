WITH FactInvoicePosition AS ( 
    SELECT 
        DIM_COUNTRY 
    FROM 
        data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED 
), 
SupplierCountry AS ( 
    SELECT 
        dim_country, 
        TXT_COUNTRY_RISK_BUCKET 
    FROM 
        data.VT_DIM_SupplierCountry 
), 
JoinedData AS ( 
    SELECT 
        fip.DIM_COUNTRY 
    FROM 
        FactInvoicePosition fip 
    LEFT OUTER JOIN 
        SupplierCountry sc 
    ON 
        fip.DIM_COUNTRY = sc.dim_country 
    WHERE 
        sc.TXT_COUNTRY_RISK_BUCKET = 'High' 
) 
SELECT 
    COUNT(DISTINCT DIM_COUNTRY) AS Count_high_risk_supplier_countries 
FROM 
    JoinedData;