    SELECT 
        YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD')) AS Year,
        ct.TXT_CATEGORY_LEVEL_2 AS Category,
        sc.txt_low_cost_country AS CostCountry, 
        ROUND(SUM(fip.MES_SPEND_CURR_1),2) AS TotalSpend
    FROM 
        data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
    JOIN 
        data.vt_dim_period p ON p.DIM_DATE = fip.DIM_DATE
    JOIN 
        data.vt_dim_suppliercountry sc ON sc.DIM_COUNTRY = fip.dim_country
    JOIN 
        data.vt_dim_supplierstatus ss ON ss.DIM_SUPPLIER_STATUS = fip.DIM_SUPPLIER_STATUS
    JOIN 
        data.vt_c_dim_valuetype vt ON vt.dim_value_type = fip.DIM_VALUE_TYPE
    JOIN 
        data.vt_c_dim_sourcingtree_techcme ct ON ct.DIM_SOURCING_TREE = fip.DIM_SOURCING_TREE
    WHERE 
        YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD')) = YEAR(CURRENT_DATE) AND
        ss.DIM_SUPPLIER_STATUS = 'E' AND
        vt.DIM_VALUE_TYPE = 'I' AND
        ct.TXT_CATEGORY_LEVEL_2 = 'Bearings' and txt_low_cost_country not in ('#')
    GROUP BY YEAR(TO_DATE(p.DIM_DATE, 'YYYYMMDD')),
        ct.TXT_CATEGORY_LEVEL_2,
        sc.txt_low_cost_country
    