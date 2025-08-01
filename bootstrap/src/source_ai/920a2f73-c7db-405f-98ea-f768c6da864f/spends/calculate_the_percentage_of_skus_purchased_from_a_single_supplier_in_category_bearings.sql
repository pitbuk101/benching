WITH FactInvoicePosition AS (
    SELECT
        m.txt_material AS Material,
        sup.TXT_CONS_SUPPLIER_L1 AS Supplier,
        year(to_date(vdp.DIM_DATE,'YYYYMMDD')) AS Year,
        ct.txt_category_level_2 AS Category
    FROM
        data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
    JOIN data.VT_DIM_Period vdp ON vdp.DIM_DATE = fip.DIM_DATE
    JOIN data.vt_dim_supplierstatus ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN data.VT_C_DIM_ValueType vt ON vt.DIM_VALUE_TYPE = fip.DIM_VALUE_TYPE
    JOIN data.vt_c_dim_material m ON fip.DIM_MATERIAL = m.DIM_MATERIAL
    JOIN data.VT_C_DIM_SourcingTree_TECHCME ct ON ct.DIM_SOURCING_TREE = fip.DIM_SOURCING_TREE
    JOIN data.VT_C_DIM_Supplier as sup ON sup.DIM_SUPPLIER = fip.dim_supplier
    WHERE
        year(to_date(vdp.dim_date,'YYYYMMDD')) = year(current_date)
        AND ss.DIM_SUPPLIER_STATUS = 'E'
        AND vt.DIM_VALUE_TYPE = 'I'
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
),
MaterialCount AS (
    SELECT
        Material,
        COUNT(DISTINCT Supplier) AS SupplierCount
    FROM
        FactInvoicePosition
    GROUP BY
        Material
),
SingleSourceMaterialCount AS (
    SELECT
        Material,
        COUNT(DISTINCT Supplier) AS SingleSourceSupplierCount
    FROM
        FactInvoicePosition
    WHERE
        Supplier IS NOT NULL
    GROUP BY
        Material
)
SELECT
    MC.Material,
    COALESCE(SSM.SingleSourceSupplierCount, 0) / NULLIF(MC.SupplierCount, 0) AS Single_Suppliers_Percentage
FROM
    MaterialCount MC
JOIN
    SingleSourceMaterialCount SSM ON MC.Material = SSM.Material;