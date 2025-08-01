WITH FilteredData AS (
    SELECT
        fip.MES_SPEND_CURR_1,
        fip.Date_dim,
        fip.DIM_COUNTRY,
        fip.DIM_SUPPLIER_STATUS,
        fip.dim_value_type,
        fip.DIM_SOURCING_TREE,
        p.YEAR_OFFSET,
        sc.txt_continent,
        ss.DIM_SUPPLIER_STATUS AS SupplierStatus,
        vt.DIM_VALUE_TYPE AS ValueType,
        ct.TXT_CATEGORY_LEVEL_2 AS CategoryLevel2
    FROM
        Fact invoice position fip
    LEFT OUTER JOIN Period p ON fip.Date_dim = p.DIM_DATE
    LEFT OUTER JOIN Supplier country sc ON fip.DIM_COUNTRY = sc.dim_country
    LEFT OUTER JOIN Supplier status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    LEFT OUTER JOIN Value type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
    LEFT OUTER JOIN Category tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE
        p.YEAR_OFFSET = 0 AND
        sc.txt_continent = 'Asia' AND
        ss.DIM_SUPPLIER_STATUS = 'E' AND
        vt.DIM_VALUE_TYPE = 'I' AND
        ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
),
AggregatedData AS (
    SELECT
        SUM(fd.MES_SPEND_CURR_1) AS TotalSpend,
        COUNT(*) AS RecordCount
    FROM
        FilteredData fd
)
SELECT
    TotalSpend,
    RecordCount
FROM
    AggregatedData;