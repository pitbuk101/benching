SELECT
    dor.TXT_ORDER_REFERENCE,
    SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
FROM
    data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
    JOIN data.vt_dim_orderreference dor ON fip.DIM_ORDER_REFERENCE = dor.DIM_ORDER_REFERENCE
    JOIN data.VT_DIM_Period vdp ON vdp.DIM_DATE = fip.DIM_DATE
    JOIN data.vt_dim_supplierstatus ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN data.VT_C_DIM_ValueType vt ON vt.DIM_VALUE_TYPE = fip.DIM_VALUE_TYPE
    JOIN data.VT_C_DIM_SourcingTree_TECHCME ct ON ct.DIM_SOURCING_TREE = fip.DIM_SOURCING_TREE
WHERE
    dor.TXT_ORDER_REFERENCE = 'Without Order Reference'
    AND year(to_date(vdp.DIM_DATE, 'YYYYMMDD')) = year(current_date)
    AND ss.DIM_SUPPLIER_STATUS = 'E'
    AND vt.DIM_VALUE_TYPE = 'I'
    AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
GROUP BY
    dor.TXT_ORDER_REFERENCE