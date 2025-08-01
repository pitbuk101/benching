WITH MaterialCount AS (
    SELECT
        m.TXT_MATERIAL,
        fip.DIM_UOM,
        AVG(fip.MES_SPEND_CURR_1) AS Price_average_delta
    FROM
        Fact invoice position fip
    JOIN
        Period p ON fip.Date_dim = p.DIM_DATE
    JOIN
        Supplier status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN
        Value type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
    JOIN
        Material m ON fip.DIM_MATERIAL = m.DIM_MATERIAL
    JOIN
        Category tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    JOIN
        Reporting currency rc ON fip.DIM_CURRENCY_COMPANY = rc.DIM_REPORTING_CURRENCY
    WHERE
        p.YEAR_OFFSET = 0
        AND ss.DIM_SUPPLIER_STATUS = 'E'
        AND vt.DIM_VALUE_TYPE = 'I'
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
        AND rc.DIM_REPORTING_CURRENCY = 'CURR_1'
    GROUP BY
        m.TXT_MATERIAL,
        fip.DIM_UOM
),
Top10SKU AS (
    SELECT
        TXT_MATERIAL,
        DIM_UOM,
        Price_average_delta
    FROM
        MaterialCount
    ORDER BY
        Price_average_delta DESC
    LIMIT 10
)
SELECT
    *
FROM
    Top10SKU;