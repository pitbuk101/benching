SELECT
    YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD')) AS YEAR,
    ct.TXT_CATEGORY_LEVEL_2 AS Category,
    m.txt_material AS Material,
    s.TXT_SUPPLIER AS Supplier,
    SUM(fip.MES_SPEND_CURR_1) AS Spends
FROM
    data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
    JOIN data.vt_dim_period p ON fip.DIM_DATE = p.DIM_DATE
    JOIN data.vt_c_dim_supplier s ON fip.DIM_SUPPLIER = s.DIM_SUPPLIER
    JOIN data.vt_dim_supplierstatus ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN data.vt_c_dim_valuetype vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
    JOIN data.vt_c_dim_material m ON fip.DIM_MATERIAL = m.DIM_MATERIAL
    JOIN data.vt_c_dim_sourcingtree_techcme ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
WHERE
    YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD')) = YEAR(CURRENT_DATE)
    AND ss.DIM_SUPPLIER_STATUS = 'E'
    AND vt.DIM_VALUE_TYPE = 'I'
    AND m.TXT_MATERIAL = 'Machining BC 2399'
    AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
GROUP BY
    YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD')),
    ct.TXT_CATEGORY_LEVEL_2,
    m.txt_material,
    s.TXT_SUPPLIER
ORDER BY Spends DESC