WITH DiffPayment AS (
SELECT 
    YEAR(TO_DATE(vdp.DIM_DATE, 'YYYYMMDD')) AS Year,
    sup.TXT_CONS_SUPPLIER_L1,
	ip.MES_DIFF_EARLY_PAYMENT,
	SUM(ip.MES_SPEND_PAID_CURR_1) AS Total_Spend,
	CASE WHEN COUNT(MES_INTEGER)>0 THEN
	SUM(MES_DIFF_EARLY_PAYMENT) / NULLIF(COUNT(MES_INTEGER), 0) 
	ELSE 0 END AS Diff_Early_Payment
FROM 
    data.VT_C_FACT_INVOICEPOSITION_PAYMENT as ip
	JOIN data.VT_C_DIM_Supplier as sup ON sup.DIM_SUPPLIER=ip.dim_supplier
	JOIN data.VT_DIM_PaymentTerm AS pt ON pt.DIM_PAYMENT_TERM = ip.DIM_PAYMENT_TERM
    JOIN data.VT_C_DIM_ValueType AS vt ON vt.DIM_VALUE_TYPE = ip.DIM_VALUE_TYPE
    JOIN data.VT_DIM_Period vdp ON vdp.DIM_DATE = ip.DIM_DATE
    WHERE vt.DIM_VALUE_TYPE = 'P' AND lower(pt.TXT_PAYMENT_TERM_TYPE) = lower('Net Payment')
    AND YEAR(TO_DATE(vdp.DIM_DATE, 'YYYYMMDD')) = YEAR(CURRENT_DATE)
    GROUP BY 
		sup.TXT_CONS_SUPPLIER_L1,
		ip.MES_DIFF_EARLY_PAYMENT,
        YEAR(TO_DATE(vdp.DIM_DATE, 'YYYYMMDD'))
		)
SELECT Year, dp.TXT_CONS_SUPPLIER_L1 as supplier,
	Total_Spend,
	Diff_Early_Payment,
	CASE WHEN dp.MES_DIFF_EARLY_PAYMENT < -3 
	THEN (dp.Total_Spend * dp.Diff_Early_Payment * -1) / 365
	ELSE 0
	END
	AS Early_Payment
FROM DiffPayment as dp
ORDER BY Early_Payment DESC