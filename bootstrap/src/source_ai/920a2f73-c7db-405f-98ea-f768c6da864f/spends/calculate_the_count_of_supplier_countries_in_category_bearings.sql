WITH PeriodFiltered AS (
    SELECT TXT_YEAR
    FROM Period
    WHERE YEAR_OFFSET = 0
),

ValueTypeFiltered AS (
    SELECT DIM_VALUE_TYPE
    FROM Value type
    WHERE DIM_VALUE_TYPE = 'I'
),

SupplierStatusFiltered AS (
    SELECT DIM_SUPPLIER_STATUS
    FROM Supplier status
    WHERE DIM_SUPPLIER_STATUS = 'E'
),

ReportingCurrencyFiltered AS (
    SELECT DIM_REPORTING_CURRENCY
    FROM Reporting currency
    WHERE DIM_REPORTING_CURRENCY = 'CURR_1'
),

CategoryTreeFiltered AS (
    SELECT TXT_CATEGORY_LEVEL_2
    FROM Category tree
    WHERE TXT_CATEGORY_LEVEL_2 = 'Bearings'
),

RegionSpend AS (
    SELECT
        p.TXT_YEAR,
        COUNT(sc.TXT_COUNTRY) AS TotalSpend
    FROM Fact invoice position fip
    JOIN PeriodFiltered p ON fip.Date_dim = p.DIM_DATE
    JOIN Supplier country sc ON fip.DIM_COUNTRY = sc.dim_country
    JOIN SupplierStatusFiltered ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN ValueTypeFiltered vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
    JOIN CategoryTreeFiltered ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE p.YEAR_OFFSET = 0
      AND ss.DIM_SUPPLIER_STATUS = 'E'
      AND vt.DIM_VALUE_TYPE = 'I'
      AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY p.TXT_YEAR
)

SELECT * FROM RegionSpend;