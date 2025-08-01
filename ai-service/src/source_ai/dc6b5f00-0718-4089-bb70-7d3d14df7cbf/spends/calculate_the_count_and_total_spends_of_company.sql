WITH CompanyInvoice AS (
SELECT
	vdc.TXT_LEVEL_4,
	fip.MES_SPEND_CURR_1
FROM
	data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
JOIN
    	data.VT_DIM_Company vdc 
    ON
	vdc.DIM_COMPANY = fip.DIM_COMPANY
WHERE
	MES_SPEND_CURR_1 IS NOT NULL
)
    SELECT 
        COUNT(DISTINCT TXT_LEVEL_4) AS Company_Distinct_Count,
        SUM(MES_SPEND_CURR_1) AS Total_Spend
    FROM 
        CompanyInvoice