WITH Fact_Invoice_Position AS (
SELECT
	sup.TXT_CONS_SUPPLIER_L1 AS Supplier,
	SUM(MES_SPEND_CURR_1) AS TotalSpend,
	COUNT(DISTINCT mes_count_invoice) AS DistinctInvoiceCount
FROM
	data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
	JOIN data.VT_C_DIM_Supplier sup
	on sup.DIM_SUPPLIER = fip.DIM_SUPPLIER
GROUP BY sup.TXT_CONS_SUPPLIER_L1 
) 
SELECT
	Supplier,
	TotalSpend / NULLIF(DistinctInvoiceCount,
	0) AS Average_Invoice_Spend
FROM
	Fact_Invoice_Position;