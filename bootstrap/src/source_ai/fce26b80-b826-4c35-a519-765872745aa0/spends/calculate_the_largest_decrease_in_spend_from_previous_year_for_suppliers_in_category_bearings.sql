WITH CategorySpend AS (
    SELECT
        year(to_date(vdp.dim_date,'YYYYMMDD')) AS Year,
        sup.TXT_SUPPLIER, 
        SUM(fip.MES_SPEND_CURR_1) AS Spend_YOY
    FROM 
       data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED as fip
        JOIN data.VT_C_DIM_Supplier as sup ON sup.DIM_SUPPLIER = fip.dim_supplier
        JOIN data.vt_dim_supplierstatus ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
        JOIN data.VT_C_DIM_SourcingTree_TECHCME as ct ON ct.DIM_SOURCING_TREE = fip.DIM_SOURCING_TREE
        JOIN data.vt_c_dim_material m ON fip.DIM_MATERIAL = m.DIM_MATERIAL
        JOIN data.VT_C_DIM_ValueType AS vt ON vt.DIM_VALUE_TYPE = fip.DIM_VALUE_TYPE
        JOIN data.VT_DIM_Period vdp ON vdp.DIM_DATE = fip.DIM_DATE
    WHERE 
        year(to_date(vdp.dim_date, 'YYYYMMDD')) = YEAR(DATEADD(YEAR, -1, CURRENT_DATE)) 
        AND ss.DIM_SUPPLIER_STATUS = 'E' 
        AND vt.DIM_VALUE_TYPE = 'I' 
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY 
        year(to_date(vdp.dim_date, 'YYYYMMDD')),
        sup.TXT_SUPPLIER
)
    SELECT 
         Year,
        TXT_SUPPLIER, 
        Spend_YOY
    FROM 
        CategorySpend
    ORDER BY 
        Spend_YOY ASC
