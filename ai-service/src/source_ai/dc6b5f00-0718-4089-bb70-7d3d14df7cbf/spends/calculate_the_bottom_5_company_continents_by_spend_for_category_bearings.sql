WITH CompanycontinentSpend AS (
    SELECT
        c.txt_continent,
        SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
    FROM
        Fact invoice position fip
    JOIN
        Company c ON fip.DIM_COMPANY = c.DIM_COMPANY
    JOIN
        Period p ON fip.Date_dim = p.DIM_DATE
    JOIN
        Supplier status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN
        Value type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
    JOIN
        Category tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE
        p.YEAR_OFFSET = 0
        AND ss.DIM_SUPPLIER_STATUS = 'E'
        AND vt.DIM_VALUE_TYPE = 'I'
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY
        c.txt_continent
),
BottomCompanycontinentSpend AS (
    SELECT
        txt_continent,
        TotalSpend
    FROM
        CompanycontinentSpend
    ORDER BY
        TotalSpend ASC
    OFFSET 0 ROWS FETCH NEXT 5 ROWS ONLY
)
SELECT
    *
FROM
    BottomCompanycontinentSpend;