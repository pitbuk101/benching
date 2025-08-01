WITH TailSpend2021 AS (
    SELECT
        sc.TXT_REGION AS Region, 
        SUM(fip.MES_SPEND_CURR_1 * 0.2) AS GroupedSpend
    FROM 
        data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
        JOIN data.VT_DIM_Period vdp ON vdp.DIM_DATE = fip.DIM_DATE
        JOIN data.vt_dim_suppliercountry sc ON fip.DIM_COUNTRY = sc.dim_country
        JOIN data.vt_dim_supplierstatus ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
        JOIN data.VT_C_DIM_ValueType vt ON vt.DIM_VALUE_TYPE = fip.DIM_VALUE_TYPE
        JOIN data.VT_C_DIM_SourcingTree_TECHCME ct ON ct.DIM_SOURCING_TREE = fip.DIM_SOURCING_TREE
    WHERE 
        year(to_date(vdp.dim_date,'YYYYMMDD')) = '2021' AND
        sc.txt_region = 'Northern America' AND
        ss.DIM_SUPPLIER_STATUS = 'E' AND
        vt.DIM_VALUE_TYPE = 'I' AND
        ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY 
        sc.TXT_REGION
),
TotalTailSpend2021 AS (
    
    SELECT SUM(GroupedSpend) AS TotalSpend2021
    FROM TailSpend2021
),
TailSpend2022 AS (
    SELECT 
        sc.TXT_REGION AS Region, 
        SUM(fip.MES_SPEND_CURR_1 * 0.2) AS GroupedSpend
    FROM 
         data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
        JOIN data.VT_DIM_Period vdp ON vdp.DIM_DATE = fip.DIM_DATE
        JOIN data.vt_dim_suppliercountry sc ON fip.DIM_COUNTRY = sc.dim_country
        JOIN data.vt_dim_supplierstatus ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
        JOIN data.VT_C_DIM_ValueType vt ON vt.DIM_VALUE_TYPE = fip.DIM_VALUE_TYPE
        JOIN data.VT_C_DIM_SourcingTree_TECHCME ct ON ct.DIM_SOURCING_TREE = fip.DIM_SOURCING_TREE
    WHERE 
        year(to_date(vdp.dim_date,'YYYYMMDD')) = '2022' AND
        sc.txt_region = 'Northern America' AND
        ss.DIM_SUPPLIER_STATUS = 'E' AND
        vt.DIM_VALUE_TYPE = 'I' AND
        ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY 
        sc.TXT_REGION
),
TotalTailSpend2022 AS (
    SELECT SUM(GroupedSpend) AS TotalSpend2022
    FROM TailSpend2022
)
SELECT 
    TotalSpend2021 AS Tail_spend_in_Northern_America_in_2021, 
    TotalSpend2022 AS Tail_spend_in_Northern_America_in_2022, 
    ((TotalSpend2022 - TotalSpend2021) / TotalSpend2021) * 100 AS Percentage_Change_in_Tail_Spend_in_Northern_America_from_2021_to_2022
FROM 
    TotalTailSpend2021, TotalTailSpend2022;