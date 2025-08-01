WITH BearingsSpend2022 AS (
    SELECT
        SUM(fip.MES_SPEND_CURR_1) AS Spend2022
    FROM
        data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
    JOIN
        data.VT_DIM_Period vdp ON vdp.DIM_DATE = fip.DIM_DATE
    JOIN
        data.vt_dim_supplierstatus ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN
        data.VT_C_DIM_ValueType vt ON vt.DIM_VALUE_TYPE = fip.DIM_VALUE_TYPE
    JOIN
        data.VT_C_DIM_SourcingTree_TECHCME ct ON ct.DIM_SOURCING_TREE = fip.DIM_SOURCING_TREE
    WHERE
        year(to_date(vdp.dim_date,'YYYYMMDD')) = '2022'
        AND ss.DIM_SUPPLIER_STATUS = 'E'
        AND vt.DIM_VALUE_TYPE = 'I'
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
),
BearingsSpend2023 AS (
    SELECT
        SUM(fip.MES_SPEND_CURR_1) AS Spend2023
    FROM
         data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
    JOIN
        data.VT_DIM_Period vdp ON vdp.DIM_DATE = fip.DIM_DATE
    JOIN
        data.vt_dim_supplierstatus ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN
        data.VT_C_DIM_ValueType vt ON vt.DIM_VALUE_TYPE = fip.DIM_VALUE_TYPE
    JOIN
        data.VT_C_DIM_SourcingTree_TECHCME ct ON ct.DIM_SOURCING_TREE = fip.DIM_SOURCING_TREE
    WHERE
        year(to_date(vdp.dim_date,'YYYYMMDD')) = '2023'
        AND ss.DIM_SUPPLIER_STATUS = 'E'
        AND vt.DIM_VALUE_TYPE = 'I'
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
)
SELECT
    bs2023.Spend2023 AS Spend_in_2023,
    bs2022.Spend2022 AS Spend_in_2022,
    ((bs2023.Spend2023 - bs2022.Spend2022) / bs2022.Spend2022) * 100 AS Percentage_Change_in_Spend_from_2022_to_2023
FROM
    BearingsSpend2022 bs2022,
    BearingsSpend2023 bs2023;