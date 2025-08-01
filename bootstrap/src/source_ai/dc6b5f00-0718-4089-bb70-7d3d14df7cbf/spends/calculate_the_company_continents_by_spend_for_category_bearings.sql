WITH CompanycontinentSpend AS (
SELECT
	c.txt_continent,
	SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
FROM
	data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
JOIN data.VT_DIM_Company AS c ON
	fip.DIM_COMPANY = c.DIM_COMPANY
JOIN data.VT_DIM_Period AS p ON
	fip.DIM_DATE = p.DIM_DATE
JOIN data.VT_DIM_SupplierStatus AS ss ON
	fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
JOIN data.VT_C_DIM_ValueType AS vt ON
	fip.dim_value_type = vt.DIM_VALUE_TYPE
JOIN data.VT_C_DIM_SourcingTree_TECHCME ct ON
	ct.DIM_SOURCING_TREE = fip.DIM_SOURCING_TREE
WHERE
	ss.DIM_SUPPLIER_STATUS = 'E'
	AND
        vt.DIM_VALUE_TYPE = 'I'
	AND
        ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
GROUP BY
	c.txt_continent
)
SELECT
	
	txt_continent,
	TotalSpend
FROM
	CompanycontinentSpend
ORDER BY
	TotalSpend DESC