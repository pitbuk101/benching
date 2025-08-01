WITH CategorySpend AS (
    SELECT
        m.TXT_MATERIAL,
        SUM(fip.MES_QUANTITY) AS Currentq_quantity,
        SUM(CASE WHEN p.DIM_DATE = DATEADD(QUARTER, -1, p.DIM_DATE) THEN fip.MES_QUANTITY ELSE 0 END) AS Prevq_quantity
    FROM
        Fact invoice position fip
        LEFT OUTER JOIN Period p ON fip.Date_dim = p.DIM_DATE
        LEFT OUTER JOIN Supplier status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
        LEFT OUTER JOIN Value type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
        LEFT OUTER JOIN Material m ON fip.DIM_MATERIAL = m.DIM_MATERIAL
        LEFT OUTER JOIN Category tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE
        p.QUARTER_OFFSET = 0
        AND ss.DIM_SUPPLIER_STATUS = 'E'
        AND vt.DIM_VALUE_TYPE = 'I'
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY
        m.TXT_MATERIAL
    HAVING
        SUM(fip.MES_QUANTITY) > 0
        AND SUM(CASE WHEN p.DIM_DATE = DATEADD(QUARTER, -1, p.DIM_DATE) THEN fip.MES_QUANTITY ELSE 0 END) > 0
        AND m.TXT_MATERIAL NOT IN ('#')
),
QoQCalculation AS (
    SELECT
        TXT_MATERIAL,
        (Currentq_quantity - Prevq_quantity) / Prevq_quantity AS QoQ%
    FROM
        CategorySpend
),
Top1 AS (
    SELECT 
        TXT_MATERIAL,
        QoQ%
    FROM
        QoQCalculation
    ORDER BY
        QoQ% ASC
)
SELECT
    TXT_MATERIAL,
    QoQ%
FROM
    Top1;