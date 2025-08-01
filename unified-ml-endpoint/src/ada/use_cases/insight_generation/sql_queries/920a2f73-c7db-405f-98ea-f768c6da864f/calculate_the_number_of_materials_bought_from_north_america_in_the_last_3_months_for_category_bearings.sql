SELECT
	ct.TXT_CATEGORY_LEVEL_2 AS Category,
	sc.txt_region AS Region,
	m.TXT_MATERIAL AS Material,
	COUNT(fip.DIM_MATERIAL) AS MaterialCount
FROM
	data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
JOIN data.VT_DIM_Period p ON p.DIM_DATE = fip.DIM_DATE 
JOIN data.VT_C_DIM_Material m ON m.DIM_MATERIAL = fip.DIM_MATERIAL 
JOIN data.VT_DIM_SupplierCountry sc ON sc.dim_country = fip.DIM_COUNTRY 
JOIN data.VT_DIM_SupplierStatus ss ON ss.DIM_SUPPLIER_STATUS = fip.DIM_SUPPLIER_STATUS 
JOIN data.VT_C_DIM_ValueType vt ON vt.DIM_VALUE_TYPE = fip.dim_value_type 
JOIN data.VT_C_DIM_SourcingTree_TECHCME ct ON ct.DIM_SOURCING_TREE = fip.DIM_SOURCING_TREE 
WHERE
	TO_DATE(p.DIM_DATE, 'YYYYMMDD') <= CURRENT_TIMESTAMP 
	AND TO_DATE(p.DIM_DATE, 'YYYYMMDD') >= DATEADD(MONTH, -3, CURRENT_TIMESTAMP)
	AND lower(sc.txt_region) = lower('Northern America')
	AND ss.DIM_SUPPLIER_STATUS = 'E'
	AND vt.DIM_VALUE_TYPE = 'I'
	AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
GROUP BY ct.TXT_CATEGORY_LEVEL_2,
	sc.txt_region,
	m.TXT_MATERIAL