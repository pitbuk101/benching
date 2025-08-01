WITH MaterialRefSpend AS (
    SELECT
        m.dim_material_reference,
        SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
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
        Reporting Currency rc ON fip.DIM_REPORTING_CURRENCY = rc.DIM_REPORTING_CURRENCY
    WHERE
        p.YEAR_OFFSET = 0
        AND vt.DIM_VALUE_TYPE = 'I'
        AND ss.DIM_SUPPLIER_STATUS = 'E'
        AND rc.DIM_REPORTING_CURRENCY = 'CURR_1'
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY
        m.dim_material_reference
),
TopMaterialRefSpend AS (
    SELECT
        dim_material_reference,
        TotalSpend
    FROM
        MaterialRefSpend
    ORDER BY
        TotalSpend DESC
    LIMIT 5
)
SELECT
    *
FROM
    TopMaterialRefSpend;