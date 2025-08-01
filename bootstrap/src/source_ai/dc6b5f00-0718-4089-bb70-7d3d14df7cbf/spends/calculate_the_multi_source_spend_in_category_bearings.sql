WITH FilteredFactInvoicePosition AS (
    SELECT
        fip.DIM_MATERIAL,
        fip.DIM_SUPPLIER,
        fip.MES_SPEND_CURR_1
    FROM
        FactInvoicePosition fip
    JOIN Period p ON fip.Date_dim = p.DIM_DATE
    JOIN SupplierStatus ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN ValueType vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
    JOIN Material m ON fip.DIM_MATERIAL = m.DIM_MATERIAL
    JOIN CategoryTree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE
        p.YEAR_OFFSET = 0
        AND ss.DIM_SUPPLIER_STATUS = 'E'
        AND vt.DIM_VALUE_TYPE = 'I'
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
),

AggregatedData AS (
    SELECT
        fip.DIM_MATERIAL,
        COUNT(DISTINCT fip.DIM_SUPPLIER) AS SupplierCount,
        SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
    FROM
        FilteredFactInvoicePosition fip
    GROUP BY
        fip.DIM_MATERIAL
)

SELECT
    ad.DIM_MATERIAL AS Material,
    ad.SupplierCount,
    ad.TotalSpend
FROM
    AggregatedData ad;