WITH FilteredData AS (
    SELECT
        fip.DIM_SUPPLIER
    FROM
        Fact invoice position fip
        LEFT OUTER JOIN Period p ON fip.Date_dim = p.DIM_DATE
        LEFT OUTER JOIN Supplier country sc ON fip.DIM_COUNTRY = sc.dim_country
        LEFT OUTER JOIN Supplier status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
        LEFT OUTER JOIN Value type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
        LEFT OUTER JOIN Category tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE
        p.YEAR_OFFSET = 0
        AND vt.DIM_VALUE_TYPE = 'I'
        AND ss.DIM_SUPPLIER_STATUS = 'E'
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
),
TotalSuppliers AS (
    SELECT
        COUNT(DISTINCT DIM_SUPPLIER) AS TotalSuppliersCount
    FROM
        FilteredData
),
LowCostCountrySuppliers AS (
    SELECT
        COUNT(DISTINCT fip.DIM_SUPPLIER) AS LowCostCountrySuppliersCount
    FROM
        Fact invoice position fip
        LEFT OUTER JOIN Period p ON fip.Date_dim = p.DIM_DATE
        LEFT OUTER JOIN Supplier country sc ON fip.DIM_COUNTRY = sc.dim_country
        LEFT OUTER JOIN Supplier status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
        LEFT OUTER JOIN Value type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
        LEFT OUTER JOIN Category tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE
        p.YEAR_OFFSET = 0
        AND sc.txt_low_cost_country = 'Low cost country'
        AND vt.DIM_VALUE_TYPE = 'I'
        AND ss.DIM_SUPPLIER_STATUS = 'E'
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
)
SELECT
    lccs.LowCostCountrySuppliersCount AS Count of suppliers from low cost countries,
    ts.TotalSuppliersCount AS Total suppliers count,
    (lccs.LowCostCountrySuppliersCount * 100.0 / ts.TotalSuppliersCount) AS Percentage of suppliers from low cost countries
FROM
    LowCostCountrySuppliers lccs,
    TotalSuppliers ts;