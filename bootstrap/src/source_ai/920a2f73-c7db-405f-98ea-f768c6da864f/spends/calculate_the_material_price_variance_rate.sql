WITH Period_CTE AS (
    SELECT
        TXT_YEAR AS TXT_YEAR,
        DIM_DATE AS DIM_DATE
    FROM Period
    WHERE TXT_YEAR IN (2022, 2023)
),

FactInvoicePosition_CTE AS (
    SELECT
        DIM_CURRENCY_COMPANY AS DIM_CURRENCY_COMPANY,
        DIM_MATERIAL AS DIM_MATERIAL,
        DIM_UOM AS DIM_UOM,
        Date_dim AS Date_dim,
        MPV_flag AS MPV_flag,
        MES_SPEND_CURR_1 AS MES_SPEND_CURR_1,
        MES_QUANTITY AS MES_QUANTITY
    FROM Fact invoice position
    WHERE MPV_flag = 'Y'
),

FilteredInvoicePosition_CTE AS (
    SELECT
        fip.DIM_CURRENCY_COMPANY,
        fip.DIM_MATERIAL,
        fip.DIM_UOM,
        fip.Date_dim,
        fip.MES_SPEND_CURR_1,
        fip.MES_QUANTITY,
        p.TXT_YEAR
    FROM FactInvoicePosition_CTE fip
    JOIN Period_CTE p ON fip.Date_dim = p.DIM_DATE n)

SELECT
    p.TXT_YEAR,
    fip.DIM_CURRENCY_COMPANY,
    fip.DIM_MATERIAL,
    fip.DIM_UOM,
    SUM(fip.MES_SPEND_CURR_1) AS Total_Spend,
    SUM(fip.MES_QUANTITY) AS Total_Quantity
FROM FilteredInvoicePosition_CTE fip
JOIN Period_CTE p ON fip.Date_dim = p.DIM_DATE
GROUP BY
    p.TXT_YEAR,
    fip.DIM_CURRENCY_COMPANY,
    fip.DIM_MATERIAL,
    fip.DIM_UOM;