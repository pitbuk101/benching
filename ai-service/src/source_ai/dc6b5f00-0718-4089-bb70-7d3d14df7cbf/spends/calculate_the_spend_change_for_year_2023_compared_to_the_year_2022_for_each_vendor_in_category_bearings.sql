WITH SupplierSpendSelectedYear AS (
SELECT
	s.TXT_SUPPLIER AS SelectedYearSupplier,
	SUM(f.MES_SPEND_CURR_1) AS SelectedYearSpend,
	YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD')) AS SelectedYear
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
	s.TXT_SUPPLIER,
	YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD'))
),
SupplierSpendTableLastYear AS (
SELECT
	s.TXT_SUPPLIER AS PreviousYearSupplier,
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
	YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD')) = YEAR(DATEADD(YEAR, -2, CURRENT_DATE))
		AND ss.DIM_SUPPLIER_STATUS = 'E'
		AND vt.DIM_VALUE_TYPE = 'I'
		AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
	GROUP BY
		s.TXT_SUPPLIER,
		YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD'))
)
SELECT
	SelectedYearSupplier,
	SelectedYear,
	ROUND(SelectedYearSpend, 2) AS SelectedYearSpend,
	PreviousYear,
	ROUND(PreviousYearSpend, 2) AS PreviousYearSpend,
	(SelectedYearSpend-PreviousYearSpend) AS ChangeInSpend,
	CONCAT(ROUND(((SelectedYearSpend-PreviousYearSpend)* 100)/ NULLIF(PreviousYearSpend, SelectedYearSpend), 2), '%') AS ChangeInSpendPercent
FROM
	SupplierSpendSelectedYear AS currents
JOIN SupplierSpendTableLastYear AS previous
ON
	currents.SelectedYearSupplier = previous.PreviousYearSupplier
WHERE
    PreviousYearSpend>0 AND SelectedYearSpend>0