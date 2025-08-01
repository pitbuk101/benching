WITH LastYearPrices AS (
    SELECT
        year(to_date(vdp.dim_date,'YYYYMMDD')) AS Year,
        ct.TXT_CATEGORY_LEVEL_2 AS Category,
        m.TXT_MATERIAL AS Material,
        u.TXT_UOM_CONS AS UOM,
        i.TXT_INCOTERM AS Incoterm,
        AVG(fip.MES_SPEND_CURR_1) AS AveragePrice
    FROM
        data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
        JOIN data.VT_DIM_Period vdp ON vdp.DIM_DATE = fip.DIM_DATE
        JOIN data.vt_dim_supplierstatus ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
        JOIN data.vt_dim_uom u ON fip.DIM_UOM = u.DIM_UOM
        JOIN data.VT_C_DIM_ValueType vt ON vt.DIM_VALUE_TYPE = fip.DIM_VALUE_TYPE
        JOIN data.vt_c_dim_material m ON fip.DIM_MATERIAL = m.DIM_MATERIAL
        JOIN data.VT_C_DIM_SourcingTree_TECHCME ct ON ct.DIM_SOURCING_TREE = fip.DIM_SOURCING_TREE
        JOIN data.vt_dim_incoterm i ON fip.DIM_INCOTERM = i.DIM_INCOTERM
    WHERE
        year(to_date(vdp.dim_date,'YYYYMMDD')) = Year(DATEADD(YEAR, -2, CURRENT_DATE)) AND
        ss.DIM_SUPPLIER_STATUS = 'E' AND
        vt.DIM_VALUE_TYPE = 'I' AND
        m.dim_material_reference = 'Material Reference' AND
        ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY
        m.TXT_MATERIAL,
        u.TXT_UOM_CONS,
        i.TXT_INCOTERM,
        year(to_date(vdp.dim_date,'YYYYMMDD')),
        ct.TXT_CATEGORY_LEVEL_2
),
TopPriceSKU AS (
    SELECT
        Year,
        Category,
        Material,
        UOM,
        Incoterm,
        AveragePrice
    FROM
        LastYearPrices
    ORDER BY
        AveragePrice DESC
)
SELECT * FROM TopPriceSKU;