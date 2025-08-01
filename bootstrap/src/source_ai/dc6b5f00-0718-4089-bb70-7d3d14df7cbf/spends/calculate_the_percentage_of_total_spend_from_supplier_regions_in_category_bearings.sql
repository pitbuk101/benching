WITH RegionSpend AS (
    SELECT 
        sc.txt_region AS Region, 
        SUM(fip.MES_SPEND_CURR_1) AS GroupedSpend
    FROM 
         data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
        JOIN data.VT_DIM_Period vdp ON vdp.DIM_DATE = fip.DIM_DATE
        JOIN data.vt_dim_suppliercountry sc ON fip.DIM_COUNTRY = sc.dim_country
        JOIN data.vt_dim_supplierstatus ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
        JOIN data.VT_C_DIM_ValueType vt ON vt.DIM_VALUE_TYPE = fip.DIM_VALUE_TYPE
        JOIN data.VT_C_DIM_SourcingTree_TECHCME ct ON ct.DIM_SOURCING_TREE = fip.DIM_SOURCING_TREE
    WHERE 
        year(to_date(vdp.DIM_DATE,'YYYYMMDD')) = year(current_date) AND
        ss.DIM_SUPPLIER_STATUS = 'E' AND
        vt.DIM_VALUE_TYPE = 'I' AND
        ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY 
        sc.txt_region
),
Top3Regions AS (
    SELECT  
        Region, 
        GroupedSpend
    FROM 
        RegionSpend
    ORDER BY 
        GroupedSpend DESC
),
Top3Spend AS (
    SELECT 
        SUM(GroupedSpend) AS Top3Spend
    FROM 
        Top3Regions
),
TotalSpend AS (
    SELECT 
        SUM(GroupedSpend) AS TotalSpend
    FROM 
        RegionSpend
)
SELECT 
    Top3Spend.Top3Spend AS Spend_from_regions, 
    TotalSpend.TotalSpend AS Total_spend, 
    (Top3Spend.Top3Spend / TotalSpend.TotalSpend) * 100 AS Percentage_of_total_spend_from_regions
FROM 
    Top3Spend, 
    TotalSpend;