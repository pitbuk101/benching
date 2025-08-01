WITH FilteredInvoices AS (
    SELECT
        fip.mes_count_invoice,
        fip.MES_SPEND_CURR_1
    FROM
        Fact_invoice_position fip
    JOIN
        Period p ON fip.Date_dim = p.DIM_DATE
    JOIN
        Supplier s ON fip.DIM_SUPPLIER = s.DIM_SUPPLIER
    JOIN
        Supplier_status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN
        Value_type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
    JOIN
        Category_tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    WHERE
        p.YEAR_OFFSET = 0
        AND s.TXT_CONS_SUPPLIER_L1 = 'SKF FRANCE'
        AND ss.DIM_SUPPLIER_STATUS = 'E'
        AND vt.DIM_VALUE_TYPE = 'I'
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
),
AggregatedInvoices AS (
    SELECT
        SUM(fip.MES_SPEND_CURR_1) AS TotalSpend,
        COUNT(fip.mes_count_invoice) AS InvoiceCount
    FROM
        FilteredInvoices fip
)
SELECT
    TotalSpend,
    InvoiceCount
FROM
    AggregatedInvoices;