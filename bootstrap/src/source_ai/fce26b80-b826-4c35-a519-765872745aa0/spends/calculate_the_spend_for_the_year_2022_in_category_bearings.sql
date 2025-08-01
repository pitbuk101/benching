WITH FilteredPeriod AS (
    SELECT *
    FROM Period
    WHERE TXT_YEAR = 2022
),
FilteredValueType AS (
    SELECT *
    FROM ValueType
    WHERE DIM_VALUE_TYPE = 'I'
),
FilteredSupplierStatus AS (
    SELECT *
    FROM SupplierStatus
    WHERE DIM_SUPPLIER_STATUS = 'E'
),
FilteredReportingCurrency AS (
    SELECT *
    FROM ReportingCurrency
    WHERE DIM_REPORTING_CURRENCY = 'CURR_1'
),
FilteredCategoryTree AS (
    SELECT *
    FROM CategoryTree
    WHERE TXT_CATEGORY_LEVEL_2 = 'Bearings'
),
FilteredFactInvoicePosition AS (
    SELECT fip.*
    FROM FactInvoicePosition fip
    JOIN FilteredPeriod p ON fip.Date_dim = p.DIM_DATE
    JOIN FilteredSupplierStatus ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN FilteredValueType vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
    JOIN FilteredCategoryTree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE p.TXT_YEAR = 2022
      AND ss.DIM_SUPPLIER_STATUS = 'E'
      AND vt.DIM_VALUE_TYPE = 'I'
      AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
)
SELECT SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
FROM FilteredFactInvoicePosition fip;