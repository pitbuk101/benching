WITH FilteredData AS (
    SELECT
        fip.MES_SPEND_CURR_1,
        fip.Date_dim,
        fip.DIM_SUPPLIER_STATUS,
        fip.dim_value_type,
        fip.DIM_MATERIAL,
        fip.DIM_SOURCING_TREE,
        p.YEAR_OFFSET,
        ss.DIM_SUPPLIER_STATUS AS SupplierStatus,
        vt.DIM_VALUE_TYPE AS ValueType,
        m.TXT_MATERIAL AS Material,
        ct.TXT_CATEGORY_LEVEL_2 AS CategoryLevel2
    FROM
        Fact invoice position fip
        LEFT OUTER JOIN Period p ON fip.Date_dim = p.DIM_DATE
        LEFT OUTER JOIN Supplier status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
        LEFT OUTER JOIN Value type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
        LEFT OUTER JOIN Material m ON fip.DIM_MATERIAL = m.DIM_MATERIAL
        LEFT OUTER JOIN Category tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE
        p.YEAR_OFFSET = 0 AND
        ss.DIM_SUPPLIER_STATUS = 'E' AND
        vt.DIM_VALUE_TYPE = 'I' AND
        m.TXT_MATERIAL = 'Machining BC 2399' AND
        ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
),
AggregatedData AS (
    SELECT
        SUM(fd.MES_SPEND_CURR_1) AS TotalSpend
    FROM
        FilteredData fd
)
SELECT
    TotalSpend
FROM
    AggregatedData;