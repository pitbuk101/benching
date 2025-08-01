WITH SKU_Supplier_Count AS ( 
    SELECT 
        Material.DIM_MATERIAL AS SKU_ID, 
        Material.TXT_MATERIAL AS SKU,
        COUNT(DISTINCT FactInvoicePosition.DIM_SUPPLIER) AS Supplier_Count
    FROM data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED AS FactInvoicePosition 
    LEFT OUTER JOIN data.VT_DIM_Period AS Period ON FactInvoicePosition.DIM_DATE = Period.DIM_DATE 
    LEFT OUTER JOIN data.VT_DIM_SupplierStatus AS SupplierStatus ON FactInvoicePosition.DIM_SUPPLIER_STATUS = SupplierStatus.DIM_SUPPLIER_STATUS 
    LEFT OUTER JOIN data.VT_C_DIM_ValueType AS ValueType ON FactInvoicePosition.dim_value_type = ValueType.DIM_VALUE_TYPE 
    LEFT OUTER JOIN data.VT_C_DIM_Material AS Material ON FactInvoicePosition.DIM_MATERIAL = Material.DIM_MATERIAL 
    LEFT OUTER JOIN data.VT_C_DIM_SourcingTree_TECHCME AS CategoryTree ON FactInvoicePosition.DIM_SOURCING_TREE = CategoryTree.DIM_SOURCING_TREE 
    WHERE 
        YEAR(CAST(Period.DIM_DATE AS DATE)) = YEAR(CURRENT_TIMESTAMP) AND 
        SupplierStatus.DIM_SUPPLIER_STATUS = 'E' AND 
        ValueType.DIM_VALUE_TYPE = 'I' AND 
        CategoryTree.TXT_CATEGORY_LEVEL_2 = 'Bearings' 
    GROUP BY Material.DIM_MATERIAL, 
        Material.TXT_MATERIAL
)
SELECT SKU AS MultiSourcedMaterialsCount
FROM SKU_Supplier_Count
WHERE Supplier_Count > 1