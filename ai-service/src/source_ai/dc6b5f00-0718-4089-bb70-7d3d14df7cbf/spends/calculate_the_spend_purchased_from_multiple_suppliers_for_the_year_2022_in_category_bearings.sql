WITH FactInvoicePosition AS (
    SELECT
        fip.DIM_MATERIAL,
        fip.DIM_SUPPLIER,
        fip.MES_SPEND_CURR_1,
        p.TXT_YEAR,
        ss.DIM_SUPPLIER_STATUS,
        vt.DIM_VALUE_TYPE,
        ct.TXT_CATEGORY_LEVEL_2
    FROM Fact_invoice_position fip
    JOIN Period p ON fip.Date_dim = p.DIM_DATE
    JOIN Supplier_status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN Value_type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
    JOIN Material m ON fip.DIM_MATERIAL = m.DIM_MATERIAL
    JOIN Category_tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE
        p.TXT_YEAR = 2022 AND
        ss.DIM_SUPPLIER_STATUS = 'E' AND
        vt.DIM_VALUE_TYPE = 'I' AND
        ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
),
SpendOnMultiSourceMaterials AS (
    SELECT
        fip.DIM_MATERIAL,
        SUM(fip.MES_SPEND_CURR_1) AS Spend_on_Multi_source_materials
    FROM FactInvoicePosition fip
    GROUP BY fip.DIM_MATERIAL
)
SELECT *
FROM SpendOnMultiSourceMaterials;