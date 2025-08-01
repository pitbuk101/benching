WITH FilteredData AS (
    SELECT
        fip.DIM_SUPPLIER
    FROM
        Fact invoice position fip
    LEFT OUTER JOIN
        Period p ON fip.Date_dim = p.DIM_DATE
    LEFT OUTER JOIN
        Supplier country sc ON fip.DIM_COUNTRY = sc.dim_country
    LEFT OUTER JOIN
        Supplier status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    LEFT OUTER JOIN
        Value type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
    LEFT OUTER JOIN
        Category tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE
        p.TXT_YEAR = 2021 AND
        sc.txt_region = 'Western Asia' AND
        ss.DIM_SUPPLIER_STATUS = 'E' AND
        vt.DIM_VALUE_TYPE = 'I' AND
        ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
),
SupplierCount AS (
    SELECT
        COUNT(DISTINCT DIM_SUPPLIER) AS SupplierCount
    FROM
        FilteredData
)
SELECT
    SupplierCount
FROM
    SupplierCount;