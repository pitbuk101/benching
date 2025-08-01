WITH SKUSpend AS (
    SELECT
        m.TXT_MATERIAL AS Material,
        SUM(fip.MES_SPEND_CURR_1) AS GroupedSpend
    FROM
        data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
         JOIN data.VT_DIM_Period vdp ON vdp.DIM_DATE = fip.DIM_DATE
         JOIN data.vt_dim_supplierstatus ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
         JOIN data.VT_C_DIM_ValueType vt ON vt.DIM_VALUE_TYPE = fip.DIM_VALUE_TYPE
         JOIN data.vt_c_dim_material m ON fip.DIM_MATERIAL = m.DIM_MATERIAL
         JOIN data.VT_C_DIM_SourcingTree_TECHCME ct ON ct.DIM_SOURCING_TREE = fip.DIM_SOURCING_TREE
    WHERE
        year(to_date(vdp.dim_date,'YYYYMMDD')) = year(current_date)
        AND ss.DIM_SUPPLIER_STATUS = 'E'
        AND vt.DIM_VALUE_TYPE = 'I'
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY
        m.TXT_MATERIAL
),
TopSKU AS (
    SELECT 
        GroupedSpend
    FROM
        SKUSpend
    ORDER BY
        GroupedSpend DESC
),
TopSKUSpend AS (
    SELECT
        SUM(GroupedSpend) AS TopSKUSpend
    FROM
        TopSKU
),
TotalSpend AS (
    SELECT
        SUM(GroupedSpend) AS TotalSpend
    FROM
        SKUSpend
),
TopSKUSpendShare AS (
    SELECT
        CASE WHEN TotalSpend.TotalSpend = 0 THEN NULL ELSE TopSKUSpend.TopSKUSpend / TotalSpend.TotalSpend END AS TopSKUSpendShare
    FROM
        TopSKUSpend,
        TotalSpend
)
SELECT
    TopSKUSpend.TopSKUSpend AS Top_SKU_spend,
    TotalSpend.TotalSpend AS Total_spend,
    TopSKUSpendShare.TopSKUSpendShare AS Share_of_total_spend_from_top_SKU
FROM
    TopSKUSpend,
    TotalSpend,
    TopSKUSpendShare;