SELECT
    YEAR(TO_DATE(fip.DIM_DATE, 'YYYYMMDD')) AS Year,
    MONTHNAME(TO_DATE(fip.DIM_DATE, 'YYYYMMDD')) AS Month_name,
    ct.TXT_CATEGORY_LEVEL_2 AS Category,
    SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
FROM
    data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
    JOIN data.VT_DIM_Period vdp ON fip.DIM_DATE = vdp.DIM_DATE
    JOIN data.vt_dim_supplierstatus ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN data.VT_C_DIM_ValueType vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
    JOIN data.vt_c_dim_sourcingtree_techcme ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
WHERE
    TO_DATE(vdp.DIM_DATE, 'YYYYMMDD') >= TO_DATE('2023-10-01', 'YYYY-MM-DD')
    AND TO_DATE(vdp.DIM_DATE, 'YYYYMMDD') <= TO_DATE('2023-12-31', 'YYYY-MM-DD')
    AND vt.DIM_VALUE_TYPE = 'I'
    AND ss.DIM_SUPPLIER_STATUS = 'E'
    AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
GROUP BY
    YEAR(TO_DATE(fip.DIM_DATE, 'YYYYMMDD')),
    MONTHNAME(TO_DATE(fip.DIM_DATE, 'YYYYMMDD')),
    ct.TXT_CATEGORY_LEVEL_2
ORDER BY
    Year, Month_name;
