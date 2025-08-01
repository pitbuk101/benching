WITH Supplier_Count AS (
    SELECT
        Year(to_date(p.date_date)) AS YEAR,
        s.TXT_SUPPLIER AS Supplier,
        fsr.TXT_DESCRIPTION AS Description,
        ct.TXT_CATEGORY_LEVEL_2 AS Category,
        SUM(fip.MES_SPEND_CURR_1) AS Spend,
        SUM(fsr.MES_RISK) AS Risk,
        (
            SUM(fsr.MES_RISK) * 1000000 + SUM(fip.MES_SPEND_CURR_1)
        ) AS Risk_key
    FROM
        data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
        JOIN data.vt_dim_period p ON fip.DIM_DATE = p.DIM_DATE
        JOIN data.vt_c_dim_supplier s ON fip.DIM_SUPPLIER = s.DIM_SUPPLIER
        JOIN data.vt_dim_supplierstatus ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
        JOIN data.vt_c_dim_valuetype vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
        JOIN data.vt_c_dim_sourcingtree_techcme ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
        JOIN data.vt_fact_risksupplier fsr ON fip.DIM_SUPPLIER = fsr.DIM_SUPPLIER
    WHERE
        year(to_date(p.dim_date, 'YYYYMMDD')) = year(current_date)
        AND ss.DIM_SUPPLIER_STATUS = 'E'
        AND vt.DIM_VALUE_TYPE = 'I'
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
        AND fsr.TXT_DESCRIPTION = 'Strucutral risk'
        AND fsr.MES_RISK IS NOT NULL
    GROUP BY
        Year(to_date(p.date_date)),
        fsr.TXT_DESCRIPTION,
        ct.TXT_CATEGORY_LEVEL_2,
        s.TXT_SUPPLIER
),
TopSupplierCount AS (
    SELECT
        Year,
        Category,
        Description,
        SUPPLIER,
        Spend,
        Risk,
        Risk_key,
        ROW_NUMBER() OVER (
            ORDER BY
                Risk_key DESC
        ) AS RowNum
    FROM
        Supplier_Count
)
SELECT
    Year,
    Category,
    Description,
    Supplier,
    Spend,
    Risk
FROM
    TopSupplierCount
WHERE
    RowNum <= 3
ORDER BY
    Spend DESC;