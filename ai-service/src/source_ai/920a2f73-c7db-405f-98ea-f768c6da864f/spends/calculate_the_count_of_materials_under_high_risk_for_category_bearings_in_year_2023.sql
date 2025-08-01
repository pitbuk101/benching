    SELECT DISTINCT
    	YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD')) AS Year,
    	TXT_CATEGORY_LEVEL_2 AS Category,
    	m.TXT_MATERIAL AS Material
    FROM
    	data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
    JOIN data.VT_DIM_Period p ON
    	p.DIM_DATE = fip.DIM_DATE
    JOIN data.VT_C_DIM_Supplier s ON
    	s.DIM_SUPPLIER = fip.DIM_SUPPLIER
    JOIN data.VT_DIM_SupplierStatus ss ON
    	ss.DIM_SUPPLIER_STATUS = fip.DIM_SUPPLIER_STATUS
    JOIN data.VT_C_DIM_ValueType vt ON
    	vt.DIM_VALUE_TYPE = fip.DIM_VALUE_TYPE
    JOIN data.VT_C_DIM_Material m ON
    	m.DIM_MATERIAL = fip.DIM_MATERIAL
    JOIN data.VT_C_DIM_SourcingTree_TECHCME ct ON
    	ct.DIM_SOURCING_TREE = fip.DIM_SOURCING_TREE
    WHERE
    	YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD')) = YEAR(CURRENT_DATE)
    	AND s.TXT_SUPPLIER_RISK_BUCKET = 'High' 
        AND vt.DIM_VALUE_TYPE = 'I' 
        AND ss.DIM_SUPPLIER_STATUS = 'E'
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'