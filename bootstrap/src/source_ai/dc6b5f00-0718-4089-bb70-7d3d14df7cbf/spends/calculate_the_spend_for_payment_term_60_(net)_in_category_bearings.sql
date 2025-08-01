WITH PaymentTerm AS (
    SELECT
        TXT_CONS_PAYMENT_TERM
    FROM
        Payment term
    WHERE
        TXT_CONS_PAYMENT_TERM = '60 (Net)'
),
Period AS (
    SELECT
        YEAR_OFFSET
    FROM
        Period
    WHERE
        YEAR_OFFSET = 0
),
ValueType AS (
    SELECT
        DIM_VALUE_TYPE
    FROM
        Value type
    WHERE
        DIM_VALUE_TYPE = 'I'
),
SupplierStatus AS (
    SELECT
        DIM_SUPPLIER_STATUS
    FROM
        Supplier status
    WHERE
        DIM_SUPPLIER_STATUS = 'E'
),
ReportingCurrency AS (
    SELECT
        DIM_REPORTING_CURRENCY
    FROM
        Reporting currency
    WHERE
        DIM_REPORTING_CURRENCY = 'CURR_1'
),
CategoryTree AS (
    SELECT
        TXT_CATEGORY_LEVEL_2
    FROM
        Category tree
    WHERE
        TXT_CATEGORY_LEVEL_2 = 'Bearings'
),
FactInvoicePosition AS (
    SELECT
        SUM(MES_SPEND_CURR_1) AS TotalSpend
    FROM
        Fact invoice position
    LEFT OUTER JOIN Period ON Fact invoice position.Date_dim = Period.DIM_DATE
    LEFT OUTER JOIN Supplier status ON Fact invoice position.DIM_SUPPLIER_STATUS = Supplier status.DIM_SUPPLIER_STATUS
    LEFT OUTER JOIN Value type ON Fact invoice position.dim_value_type = Value type.DIM_VALUE_TYPE
    LEFT OUTER JOIN Category tree ON Fact invoice position.DIM_SOURCING_TREE = Category tree.DIM_SOURCING_TREE
    LEFT OUTER JOIN Payment term ON Fact invoice position.DIM_PAYMENT_TERM = Payment term.DIM_PAYMENT_TERM
    WHERE
        Period.YEAR_OFFSET = 0
        AND Supplier status.DIM_SUPPLIER_STATUS = 'E'
        AND Value type.DIM_VALUE_TYPE = 'I'
        AND Category tree.TXT_CATEGORY_LEVEL_2 = 'Bearings'
        AND Payment term.TXT_CONS_PAYMENT_TERM = '60 (Net)'
)
SELECT
    PaymentTerm.TXT_CONS_PAYMENT_TERM,
    Period.YEAR_OFFSET,
    ValueType.DIM_VALUE_TYPE,
    SupplierStatus.DIM_SUPPLIER_STATUS,
    ReportingCurrency.DIM_REPORTING_CURRENCY,
    CategoryTree.TXT_CATEGORY_LEVEL_2,
    FactInvoicePosition.TotalSpend
FROM
    PaymentTerm,
    Period,
    ValueType,
    SupplierStatus,
    ReportingCurrency,
    CategoryTree,
    FactInvoicePosition;