WITH FilteredPeriod AS (
    SELECT TXT_QUARTER
    FROM Period
    WHERE TXT_QUARTER = '2022 Q4'
),
FilteredValueType AS (
    SELECT DIM_VALUE_TYPE
    FROM Value type
    WHERE DIM_VALUE_TYPE = 'I'
),
FilteredSupplierStatus AS (
    SELECT DIM_SUPPLIER_STATUS
    FROM Supplier status
    WHERE DIM_SUPPLIER_STATUS = 'E'
),
FilteredReportingCurrency AS (
    SELECT DIM_REPORTING_CURRENCY
    FROM Reporting currency
    WHERE DIM_REPORTING_CURRENCY = 'CURR_1'
),
FilteredCategoryTree AS (
    SELECT TXT_CATEGORY_LEVEL_2
    FROM Category tree
    WHERE TXT_CATEGORY_LEVEL_2 = 'Bearings'
)
SELECT
    SUM(Fact invoice position.MES_SPEND_CURR_1) AS TotalSpend
FROM
    Fact invoice position
    LEFT OUTER JOIN Period ON Fact invoice position.Date_dim = Period.DIM_DATE
    LEFT OUTER JOIN Supplier status ON Fact invoice position.DIM_SUPPLIER_STATUS = Supplier status.DIM_SUPPLIER_STATUS
    LEFT OUTER JOIN Value type ON Fact invoice position.dim_value_type = Value type.DIM_VALUE_TYPE
    LEFT OUTER JOIN Category tree ON Fact invoice position.DIM_SOURCING_TREE = Category tree.DIM_SOURCING_TREE
WHERE
    Period.TXT_QUARTER = '2022 Q4'
    AND Supplier status.DIM_SUPPLIER_STATUS = 'E'
    AND Value type.DIM_VALUE_TYPE = 'I'
    AND Category tree.TXT_CATEGORY_LEVEL_2 = 'Bearings';