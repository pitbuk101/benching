WITH FilteredData AS (
    SELECT
        fip.MES_SPEND_CURR_1,
        year(to_date(vdp.DIM_DATE,'YYYYMMDD')) AS Year,
        uom.TXT_UOM_CONS AS UOM,
        ct.TXT_CATEGORY_LEVEL_2 AS Category
    FROM
        data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
     JOIN data.VT_DIM_Period vdp ON fip.DIM_DATE = vdp.DIM_DATE
     JOIN data.vt_dim_supplierstatus ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
     JOIN data.vt_dim_uom uom ON fip.DIM_UOM = uom.DIM_UOM
     JOIN data.VT_C_DIM_ValueType vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
     JOIN data.vt_c_dim_sourcingtree_techcme ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE
        year(to_date(vdp.DIM_DATE,'YYYYMMDD')) = '2023' AND
        ss.DIM_SUPPLIER_STATUS = 'E' AND
        uom.TXT_UOM_CONS = 'KG' AND
        vt.DIM_VALUE_TYPE = 'I' AND
        ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
)
    SELECT
        UOM,
        Category,
        SUM(fd.MES_SPEND_CURR_1) AS TotalSpend,
    FROM
        FilteredData fd
    GROUP BY
        UOM,Category
