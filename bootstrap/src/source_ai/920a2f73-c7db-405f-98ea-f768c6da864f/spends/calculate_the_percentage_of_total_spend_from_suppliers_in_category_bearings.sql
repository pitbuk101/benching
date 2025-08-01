WITH SupplierSpend AS (
    SELECT
        s.TXT_CONS_SUPPLIER_L1 AS Supplier,
        SUM(fip.MES_SPEND_CURR_1) AS GroupedSpend
    FROM
        data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
        JOIN data.VT_DIM_Period vdp ON vdp.DIM_DATE = fip.DIM_DATE
        JOIN data.vt_c_dim_supplier s ON fip.DIM_SUPPLIER = s.DIM_SUPPLIER
        JOIN data.vt_dim_supplierstatus ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
        JOIN data.VT_C_DIM_ValueType vt ON vt.DIM_VALUE_TYPE = fip.DIM_VALUE_TYPE
        JOIN data.VT_C_DIM_SourcingTree_TECHCME ct ON ct.DIM_SOURCING_TREE = fip.DIM_SOURCING_TREE
    WHERE
        year(to_date(vdp.DIM_DATE,'YYYYMMDD')) = year(current_date)
        AND ss.DIM_SUPPLIER_STATUS = 'E'
        AND vt.DIM_VALUE_TYPE = 'I'
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
    GROUP BY
        s.TXT_CONS_SUPPLIER_L1
),
Top5Suppliers AS (
    SELECT 
        Supplier,
        GroupedSpend
    FROM
        SupplierSpend
    ORDER BY
        GroupedSpend DESC
),
Top5Spend AS (
    SELECT
        SUM(GroupedSpend) AS Top5Spend
    FROM
        Top5Suppliers
),
TotalSpend AS (
    SELECT
        SUM(GroupedSpend) AS TotalSpend
    FROM
        SupplierSpend
)
SELECT
    Top5Spend.Top5Spend AS Spend_from_suppliers,
    TotalSpend.TotalSpend AS Total_spend,
    (Top5Spend.Top5Spend / TotalSpend.TotalSpend) * 100 AS Percentage_of_total_spend_from_suppliers
FROM
    Top5Spend,
    TotalSpend;