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
SpendHighRiskL1Suppliers AS (
    SELECT Period.TXT_YEAR,
           SUM(Fact invoice position.MES_SPEND_CURR_1) AS High Spend
    FROM Fact invoice position
    JOIN Period ON Fact invoice position.Date_dim = Period.DIM_DATE
    JOIN Supplier ON Fact invoice position.DIM_SUPPLIER = Supplier.DIM_SUPPLIER
    JOIN Supplier status ON Fact invoice position.DIM_SUPPLIER_STATUS = Supplier status.DIM_SUPPLIER_STATUS
    JOIN Value type ON Fact invoice position.dim_value_type = Value type.DIM_VALUE_TYPE
    JOIN Category tree ON Fact invoice position.DIM_SOURCING_TREE = Category tree.DIM_SOURCING_TREE
    WHERE Period.YEAR_OFFSET = 0
      AND Supplier status.DIM_SUPPLIER_STATUS = 'E'
      AND Value type.DIM_VALUE_TYPE = 'I'
      AND Category tree.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY Period.TXT_YEAR
)
SELECT *
FROM SpendHighRiskL1Suppliers;