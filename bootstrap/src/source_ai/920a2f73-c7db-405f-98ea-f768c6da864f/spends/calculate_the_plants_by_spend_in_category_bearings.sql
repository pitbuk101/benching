WITH PlantSpend AS (
    SELECT
        p.TXT_PLANT,
        SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
    FROM
        Fact invoice position fip
        LEFT OUTER JOIN Period pr ON fip.Date_dim = pr.DIM_DATE
        LEFT OUTER JOIN Supplier status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
        LEFT OUTER JOIN Value type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
        LEFT OUTER JOIN Category tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
        LEFT OUTER JOIN Plant p ON fip.DIM_PLANT = p.DIM_PLANT
    WHERE
        pr.YEAR_OFFSET = 0
        AND ss.DIM_SUPPLIER_STATUS = 'E'
        AND vt.DIM_VALUE_TYPE = 'I'
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY
        p.TXT_PLANT
),
TopPlantSpend AS (
    SELECT
        *
    FROM
        PlantSpend
    ORDER BY
        TotalSpend DESC
    OFFSET 0 ROWS FETCH NEXT 5 ROWS ONLY
)
SELECT
    *
FROM
    TopPlantSpend;