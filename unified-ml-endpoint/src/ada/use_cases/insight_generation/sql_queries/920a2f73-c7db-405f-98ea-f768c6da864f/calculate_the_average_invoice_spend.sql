WITH Fact_Invoice_Position AS (
SELECT
	SUM(MES_SPEND_CURR_1) AS TotalSpend,
	COUNT(DISTINCT mes_count_invoice) AS DistinctInvoiceCount
FROM
	data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED
) 
SELECT
	TotalSpend / NULLIF(DistinctInvoiceCount,
	0) AS Average_Invoice_Spend
FROM
	Fact_Invoice_Position;