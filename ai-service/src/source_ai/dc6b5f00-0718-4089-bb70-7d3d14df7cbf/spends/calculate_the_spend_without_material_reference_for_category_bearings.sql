SELECT
    m.dim_material_reference,
    SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
FROM
    data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
    JOIN data.VT_DIM_Period vdp ON vdp.DIM_DATE = fip.DIM_DATE
    JOIN data.vt_dim_supplierstatus ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN data.VT_C_DIM_ValueType vt ON vt.DIM_VALUE_TYPE = fip.DIM_VALUE_TYPE
    JOIN data.VT_C_DIM_SourcingTree_TECHCME ct ON ct.DIM_SOURCING_TREE = fip.DIM_SOURCING_TREE
    JOIN data.vt_c_dim_material m ON fip.DIM_MATERIAL = m.DIM_MATERIAL
WHERE
    year(to_date(vdp.DIM_DATE, 'YYYYMMDD')) = year(current_date)
    AND ss.DIM_SUPPLIER_STATUS = 'E'
    AND vt.DIM_VALUE_TYPE = 'I'
    AND m.dim_material_reference = 'No Material Reference'
    AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
GROUP BY
    m.dim_material_reference;