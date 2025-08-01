WITH SubCategorySpend AS (
    SELECT
        ct.TXT_CATEGORY_LEVEL_2,
        SUM(fip.MES_SPEND_CURR_1) AS GroupedSpend
    FROM
        Fact invoice position fip
    LEFT OUTER JOIN Period p ON fip.Date_dim = p.DIM_DATE
    LEFT OUTER JOIN Supplier status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    LEFT OUTER JOIN Value type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
    LEFT OUTER JOIN Category tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE
        p.YEAR_OFFSET = 0 AND
        ss.DIM_SUPPLIER_STATUS = 'E' AND
        vt.DIM_VALUE_TYPE = 'I' AND
        ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY
        ct.TXT_CATEGORY_LEVEL_2
),
TotalSpend AS (
    SELECT SUM(GroupedSpend) AS TotalSpend FROM SubCategorySpend
),
RunningSpend AS (
    SELECT
        scs.TXT_CATEGORY_LEVEL_2,
        scs.GroupedSpend,
        SUM(scs.GroupedSpend) OVER (ORDER BY scs.GroupedSpend DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / ts.TotalSpend AS RunningPercSpend
    FROM
        SubCategorySpend scs,
        TotalSpend ts
),
Top70SpendSubCategoriesCount AS (
    SELECT COUNT(*) AS Top70Count FROM RunningSpend WHERE RunningPercSpend < 0.70
)
SELECT Top70Count AS Number of sub-categories covering 70% of spend FROM Top70SpendSubCategoriesCount;