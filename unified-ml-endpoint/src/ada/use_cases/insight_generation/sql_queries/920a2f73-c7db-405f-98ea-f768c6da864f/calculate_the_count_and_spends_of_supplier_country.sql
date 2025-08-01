WITH SupplierCountry AS ( 
    SELECT 
        TXT_COUNTRY AS Country, 
        COUNT(*) AS CountryCount 
    FROM 
        data.VT_DIM_SupplierCountry 
    GROUP BY 
        TXT_COUNTRY 
), 
FactInvoicePosition AS ( 
    SELECT 
        TXT_COUNTRY AS Country, 
        SUM(MES_SPEND_CURR_1) AS TotalSpend, 
        COUNT(*) AS InvoiceCount 
    FROM 
        data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED 
    JOIN 
        data.VT_DIM_SupplierCountry ON data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED.DIM_COUNTRY = data.VT_DIM_SupplierCountry.dim_country 
    GROUP BY 
        TXT_COUNTRY 
) 
SELECT 
    sc.Country, 
    sc.CountryCount, 
    fip.TotalSpend, 
    fip.InvoiceCount 
FROM 
    SupplierCountry sc 
JOIN 
    FactInvoicePosition fip ON sc.Country = fip.Country;