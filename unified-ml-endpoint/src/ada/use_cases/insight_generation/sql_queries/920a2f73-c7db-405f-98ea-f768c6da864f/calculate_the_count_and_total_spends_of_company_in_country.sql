WITH CompanyCountry AS (
SELECT
	TXT_COUNTRY
FROM
	data.VT_DIM_Company 
), 
FactInvoicePosition AS (
SELECT
	c.TXT_COUNTRY,
	SUM(fip.MES_SPEND_CURR_1) AS TotalSpend,
	COUNT(DIM_INVOICE_POSITION) AS InvoiceCount
FROM
	data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
JOIN 
        data.VT_DIM_Company c ON
	fip.DIM_COMPANY = c.DIM_COMPANY
GROUP BY
	c.TXT_COUNTRY 
), 
FilteredCompanyCountry AS (
SELECT
	TXT_COUNTRY
FROM
	data.VT_DIM_Company
)
SELECT 
	distinct
    cc.TXT_COUNTRY AS Country, 
    fip.TotalSpend AS Total_Spend, 
    fip.InvoiceCount AS Count_Invoice
FROM 
    CompanyCountry cc 
JOIN 
    FactInvoicePosition fip ON cc.TXT_COUNTRY = fip.TXT_COUNTRY 
JOIN 
    FilteredCompanyCountry fcc ON cc.TXT_COUNTRY = fcc.TXT_COUNTRY 
ORDER BY Total_Spend DESC