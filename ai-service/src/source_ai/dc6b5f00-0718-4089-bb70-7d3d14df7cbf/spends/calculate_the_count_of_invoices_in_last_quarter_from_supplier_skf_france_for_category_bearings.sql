with selectedQuarter AS (
 SELECT min(TO_DATE(p.DIM_DATE, 'YYYYMMDD')) as min_date, max(TO_DATE(p.DIM_DATE, 'YYYYMMDD')) as max_date
 FROM data.VT_DIM_Period as p
 WHERE YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD')) = YEAR(CURRENT_TIMESTAMP)
 AND DATEPART(QUARTER, TO_DATE(p.DIM_DATE, 'YYYYMMDD')) = QUARTER(CURRENT_TIMESTAMP)
)
SELECT
	p.TXT_QUARTER AS CurrentQuarter,
	ct.TXT_CATEGORY_LEVEL_2 AS Category,
	s.TXT_SUPPLIER AS Supplier,
	COUNT(fip.DIM_INVOICE_POSITION) AS InvoiceCount
FROM
	data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
JOIN 
        data.VT_DIM_Period p ON
	p.DIM_DATE = fip.DIM_DATE
JOIN 
        data.VT_C_DIM_Supplier s ON
	s.DIM_SUPPLIER = fip.DIM_SUPPLIER
JOIN 
        data.VT_DIM_SupplierStatus ss ON
	ss.DIM_SUPPLIER_STATUS = fip.DIM_SUPPLIER_STATUS
JOIN 
        data.VT_C_DIM_ValueType vt ON
	vt.dim_value_type = fip.DIM_VALUE_TYPE
JOIN 
        data.VT_C_DIM_SourcingTree_TECHCME ct ON
	ct.DIM_SOURCING_TREE = fip.DIM_SOURCING_TREE
WHERE
	 TO_DATE(p.DIM_DATE, 'YYYYMMDD') = (select min_date from selectedQuarter)
 AND TO_DATE(p.DIM_DATE, 'YYYYMMDD') = (select max_date from selectedQuarter)
	AND 
        lower(s.TXT_SUPPLIER) = lower('SKF FRANCE')
	AND 
        ss.DIM_SUPPLIER_STATUS = 'E'
	AND 
        vt.DIM_VALUE_TYPE = 'I'
	AND 
        ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
GROUP BY p.TXT_QUARTER,
	ct.TXT_CATEGORY_LEVEL_2,
	s.TXT_SUPPLIER