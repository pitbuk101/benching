WITH IncotermSpend AS (
    SELECT 
        Incoterm.TXT_INCOTERM,
        SUM(FactInvoicePosition.MES_SPEND_CURR_1) AS TotalSpend
    FROM 
        FactInvoicePosition
    JOIN 
        Period ON FactInvoicePosition.Date_dim = Period.DIM_DATE
    JOIN 
        SupplierStatus ON FactInvoicePosition.DIM_SUPPLIER_STATUS = SupplierStatus.DIM_SUPPLIER_STATUS
    JOIN 
        ValueType ON FactInvoicePosition.dim_value_type = ValueType.DIM_VALUE_TYPE
    JOIN 
        CategoryTree ON FactInvoicePosition.DIM_SOURCING_TREE = CategoryTree.DIM_SOURCING_TREE
    JOIN 
        Incoterm ON FactInvoicePosition.DIM_INCOTERM = Incoterm.DIM_INCOTERM
    WHERE 
        Period.YEAR_OFFSET = 0
        AND SupplierStatus.DIM_SUPPLIER_STATUS = 'E'
        AND ValueType.DIM_VALUE_TYPE = 'I'
        AND CategoryTree.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY 
        Incoterm.TXT_INCOTERM
),
BottomIncotermSpend AS (
    SELECT 
        TXT_INCOTERM, 
        TotalSpend
    FROM 
        IncotermSpend
    ORDER BY 
        TotalSpend ASC
    LIMIT 5
)
SELECT 
    *
FROM 
    BottomIncotermSpend;