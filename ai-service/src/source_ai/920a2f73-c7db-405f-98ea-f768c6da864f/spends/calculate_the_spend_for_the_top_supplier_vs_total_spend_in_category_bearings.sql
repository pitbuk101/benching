WITH SupplierSpend AS (
    SELECT
        s.DIM_SUPPLIER,
        s.TXT_CONS_SUPPLIER_L1,
        SUM(fip.MES_SPEND_CURR_1) AS GroupedSpend
    FROM
        Fact_invoice_position fip
        JOIN Period p ON fip.Date_dim = p.DIM_DATE
        JOIN Supplier s ON fip.DIM_SUPPLIER = s.DIM_SUPPLIER
        JOIN Supplier_status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
        JOIN Value_type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
        JOIN Category_tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE
        p.YEAR_OFFSET = 0
        AND vt.DIM_VALUE_TYPE = 'I'
        AND ss.DIM_SUPPLIER_STATUS = 'E'
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY
        s.DIM_SUPPLIER,
        s.TXT_CONS_SUPPLIER_L1
),
TopSupplier AS (
    SELECT 
        DIM_SUPPLIER,
        TXT_CONS_SUPPLIER_L1,
        GroupedSpend
    FROM
        SupplierSpend
    ORDER BY
        GroupedSpend DESC
),
TopSupplierSpend AS (
    SELECT
        SUM(GroupedSpend) AS TopSupplierSpend
    FROM
        TopSupplier
),
TotalSpend AS (
    SELECT
        SUM(GroupedSpend) AS TotalSpend
    FROM
        SupplierSpend
)
SELECT
    ts.TopSupplierSpend,
    ts2.TotalSpend
FROM
    TopSupplierSpend ts,
    TotalSpend ts2;