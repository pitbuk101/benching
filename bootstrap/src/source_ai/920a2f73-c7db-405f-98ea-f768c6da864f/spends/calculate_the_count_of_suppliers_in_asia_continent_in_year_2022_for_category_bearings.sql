SELECT
	DISTINCT
	ct.TXT_CATEGORY_LEVEL_2 AS Category,
	sc.txt_continent AS Continent,
	s.TXT_CONS_SUPPLIER_L1 AS Supplier
FROM
	data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
JOIN data.VT_DIM_Period p ON p.DIM_DATE = fip.DIM_DATE 
JOIN data.VT_C_DIM_Supplier s ON s.DIM_SUPPLIER = fip.DIM_SUPPLIER 
JOIN data.VT_DIM_SupplierCountry sc ON sc.dim_country = fip.DIM_COUNTRY 
JOIN data.VT_DIM_SupplierStatus ss ON ss.DIM_SUPPLIER_STATUS = fip.DIM_SUPPLIER_STATUS 
JOIN data.VT_C_DIM_ValueType vt ON vt.DIM_VALUE_TYPE = fip.dim_value_type 
JOIN data.VT_C_DIM_SourcingTree_TECHCME ct ON ct.DIM_SOURCING_TREE = fip.DIM_SOURCING_TREE 
WHERE
	YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD'))= '2022'
	AND lower(sc.txt_continent) = lower('Asia')
	AND ss.DIM_SUPPLIER_STATUS = 'E'
	AND vt.DIM_VALUE_TYPE = 'I'
	AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'