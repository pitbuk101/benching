WITH SupplierSpendCurrentYear AS (
SELECT
	s.TXT_CONS_SUPPLIER_L1 AS CurrentYearSupplier,
	SUM(f.MES_SPEND_CURR_1) AS CurrentYearSpend,
	YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD')) AS CurrentYear
FROM
	data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED f
JOIN data.VT_DIM_Period p ON
	f.DIM_DATE = p.DIM_DATE
JOIN data.VT_C_DIM_Supplier s ON
	f.DIM_SUPPLIER = s.DIM_SUPPLIER
JOIN data.VT_DIM_SupplierStatus ss ON
	f.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
JOIN data.VT_C_DIM_ValueType vt ON
	f.dim_value_type = vt.DIM_VALUE_TYPE
JOIN data.VT_C_DIM_SourcingTree_TECHCME ct ON
	f.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
WHERE
	YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD')) = YEAR(CURRENT_DATE)
	AND ss.DIM_SUPPLIER_STATUS = 'E'
	AND vt.DIM_VALUE_TYPE = 'I'
	AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
GROUP BY
	s.TXT_CONS_SUPPLIER_L1,
	YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD'))
),
SupplierSpendTableLastYear AS (
SELECT
	s.TXT_CONS_SUPPLIER_L1 AS PreviousYearSupplier,
	SUM(f.MES_SPEND_CURR_1) AS PreviousYearSpend,
	YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD')) AS PreviousYear
FROM
	data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED f
JOIN data.VT_DIM_Period p ON
	f.DIM_DATE = p.DIM_DATE
JOIN data.VT_C_DIM_Supplier s ON
	f.DIM_SUPPLIER = s.DIM_SUPPLIER
JOIN data.VT_DIM_SupplierStatus ss ON
	f.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
JOIN data.VT_C_DIM_ValueType vt ON
	f.dim_value_type = vt.DIM_VALUE_TYPE
JOIN data.VT_C_DIM_SourcingTree_TECHCME ct ON
	f.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
WHERE
		YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD')) = YEAR(DATEADD(YEAR, -1, CURRENT_DATE))
		AND ss.DIM_SUPPLIER_STATUS = 'E'
		AND vt.DIM_VALUE_TYPE = 'I'
		AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings' 
	GROUP BY
		s.TXT_CONS_SUPPLIER_L1,
		YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD'))
)
SELECT
	CurrentYearSupplier,
	CurrentYear,
	ROUND(CurrentYearSpend, 2) AS CurrentYearSpend,
	PreviousYear,
	ROUND(PreviousYearSpend, 2) AS PreviousYearSpend,
	(CurrentYearSpend-PreviousYearSpend) AS ChangeInSpend,
	CONCAT(ROUND(((CurrentYearSpend-PreviousYearSpend)* 100)/ NULLIF(PreviousYearSpend, CurrentYearSpend), 2), '%') AS ChangeInSpendPercent
FROM
	SupplierSpendCurrentYear AS currents
JOIN SupplierSpendTableLastYear AS previous
ON
	currents.CurrentYearSupplier = previous.PreviousYearSupplier
WHERE CurrentYearSpend>0 and PreviousYearSpend>0