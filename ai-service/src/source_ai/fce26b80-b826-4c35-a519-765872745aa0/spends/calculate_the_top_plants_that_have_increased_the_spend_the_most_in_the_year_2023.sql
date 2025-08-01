with PlantSpendSelectedYear AS (
SELECT
	plant.TXT_PLANT AS SelectedYearPlants,
	SUM(f.MES_SPEND_CURR_1) AS SelectedYearSpend,
	YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD')) AS SelectedYear
FROM
	data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED f
JOIN data.VT_DIM_Period p ON
	p.DIM_DATE = f.DIM_DATE
JOIN data.VT_DIM_Plant plant ON
	plant.DIM_PLANT = f.DIM_PLANT
JOIN data.VT_DIM_SupplierStatus ss ON
	ss.DIM_SUPPLIER_STATUS = f.DIM_SUPPLIER_STATUS
JOIN data.VT_C_DIM_ValueType vt ON
	vt.DIM_VALUE_TYPE = f.DIM_VALUE_TYPE
JOIN data.VT_C_DIM_SourcingTree_TECHCME ct ON
	ct.DIM_SOURCING_TREE = f.DIM_SOURCING_TREE
WHERE
	YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD')) = YEAR(CAST('2023' AS DATE))
	AND ss.DIM_SUPPLIER_STATUS = 'E'
	AND vt.DIM_VALUE_TYPE = 'I'
	AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
GROUP BY
	plant.TXT_PLANT,
	YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD'))
),
PlantSpendLastYear AS (
SELECT
	plant.TXT_PLANT AS PreviousYearPlants,
	SUM(f.MES_SPEND_CURR_1) AS PreviousYearSpend,
	YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD')) AS PreviousYear
FROM
	data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED f
JOIN data.VT_DIM_Period p ON
	p.DIM_DATE = f.DIM_DATE
JOIN data.VT_DIM_Plant plant ON
	plant.DIM_PLANT = f.DIM_PLANT
JOIN data.VT_DIM_SupplierStatus ss ON
	ss.DIM_SUPPLIER_STATUS = f.DIM_SUPPLIER_STATUS
JOIN data.VT_C_DIM_ValueType vt ON
	vt.DIM_VALUE_TYPE = f.DIM_VALUE_TYPE
JOIN data.VT_C_DIM_SourcingTree_TECHCME ct ON
	ct.DIM_SOURCING_TREE = f.DIM_SOURCING_TREE
WHERE
	YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD')) = YEAR(DATEADD(YEAR, -1, CAST('2023' AS DATE)))
	AND ss.DIM_SUPPLIER_STATUS = 'E'
	AND vt.DIM_VALUE_TYPE = 'I'
	AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
GROUP BY
	plant.TXT_PLANT,
	YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD'))
)
SELECT
	SelectedYearPlants,
	SelectedYear,
	ROUND(SelectedYearSpend, 2) AS SelectedYearSpend,
	PreviousYear,
	ROUND(PreviousYearSpend, 2) AS PreviousYearSpend,
	(SelectedYearSpend-PreviousYearSpend) AS ChangeInSpend,
	CONCAT(ROUND(((SelectedYearSpend-PreviousYearSpend)* 100)/ NULLIF(PreviousYearSpend, SelectedYearSpend), 2), '%') AS ChangeInSpendPercent
FROM PlantSpendSelectedYear AS currents
JOIN PlantSpendLastYear AS previous
ON currents.SelectedYearPlants = previous.PreviousYearPlants
ORDER BY ChangeInSpendPercent DESC